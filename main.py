from typing import List, Tuple
from gerarPDF import gerar_relatorio
import pandas as pd
import os
import re

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(currentDir)
csvDir = os.path.join(parentDir, "source")


def tokens_treatment(filename: str) -> List[str]:
    base = os.path.splitext(os.path.basename(filename))[0]
    words = re.findall(r"[A-Za-z0-9']+", base)
    lower_words = [w.lower() for w in words]
    platforms = ["tiktok", "google", "meta"]
    stopwords = {"ad", "report"}

    idx_platform = len(words)
    for p in platforms:
        if p in lower_words:
            idx_platform = min(idx_platform, lower_words.index(p))

    useful_words = [
        w for w in words[:idx_platform]
        if w.lower() not in stopwords
    ]
    return useful_words

def guess_client_and_campaign(filenames: List[str]) -> Tuple[str, str]:
    """
    Retorna:
      - nome do cliente (string)
      - nome da campanha (string): primeiro termo não vazio
    """
    per_file_words = {f: tokens_treatment(f) for f in filenames}

    # interseção para achar o cliente
    sets_lower = [{w.lower() for w in words} for words in per_file_words.values()]
    common_lower = set.intersection(*sets_lower)

    # ordena e preserva capitalização usando o primeiro arquivo
    first_words = per_file_words[filenames[0]]
    client_tokens = [w for w in first_words if w.lower() in common_lower]
    client_name = " ".join(client_tokens)

    # campanhas individuais
    campaign_list = []
    for words in per_file_words.values():
        leftover = [w for w in words if w.lower() not in common_lower]
        campaign_list.append(" ".join(leftover).strip())

    # pega o primeiro nome de campanha não vazio
    campaign_name = next((c for c in campaign_list if c.strip()), "")

    return client_name, campaign_name


colsMeta = [
    "Clicks (all)",
    "Link clicks",
    "CTR (link click-through rate)",
    "CPC (cost per link click) (USD)",
    "Page engagement",
    "Views",
    "3-second video plays",

    #extras
    "Ad name"
]

colsGoogle = [
    "Clicks",
    "CTR",
    "Engagements",
    "Engagement rate",
    "Watch time",
    "Avg. watch time / impr.",
    "Video played to 25%",
    "Video played to 50%",
    "Video played to 75%",
    "Video played to 100%",

    #extras
    "Video"
]

colsTiktok = [
    "Clicks (all)",
    "CTR (all)",
    "CPC (destination)",
    "Video views",
    "Video views at 100%",
    "Average play time per video view"

    #extras
    "Ad name"
]

dfList = []

for file in os.listdir(csvDir):
    full_path = os.path.join(csvDir, file)
    print(f"\n=== Processando arquivo: {file} ===")
    header = 0

    # Decide fonte, colunas e encoding
    if "META" in file.upper():
        cols = colsMeta
        source = "Meta"
        encoding = "utf-8"
        skiprows = 0
        sep = ","
    elif "GOOGLE" in file.upper():
        cols = colsGoogle
        source = "Google"
        encoding = "utf-16"
        skiprows = 2
        sep = "\t"
    elif "TIKTOK" in file.upper():
        cols = colsTiktok
        source = "TikTok"
        encoding = None
        skiprows = 0
    else:
        continue

    if file.lower().endswith(".csv"):
        header_df = pd.read_csv(
            full_path,
            encoding=encoding,
            skiprows=skiprows,
            nrows=0,
            sep=sep
        )

        df = pd.read_csv(full_path, encoding=encoding ,sep=sep ,header=skiprows)
        # print(df.head())
        df.columns = df.columns.str.strip()               # remove espaços
        df.columns = df.columns.str.replace('\ufeff','')  # remove BOM invisível
        df.columns = df.columns.str.replace('\u200b','')  # remove espaço zero-width
        df.columns = df.columns.str.replace('\n','')      # remove quebras
        df.columns = df.columns.str.replace('\r','')
        df.columns = df.columns.str.replace('"','')
        drop_cols = [c for c in header_df.columns if c not in cols]
        print(df.head())
        # print(df.columns.tolist())
        df = df.drop(columns=drop_cols)


    elif file.lower().endswith(".xlsx"):
        header = pd.read_excel(full_path, nrows=0).columns
        print("  Header encontrado:", list(header))

        cols_to_use = [c for c in cols if c in header]
        print("  Colunas a usar:", cols_to_use)

        df = pd.read_excel(full_path, usecols=cols_to_use)

    else:
        continue

    print(df.head())
    dfList.append((source, df))



filenames = [
f for f in os.listdir(csvDir)
if f.lower().endswith((".csv", ".xlsx"))
]

client_name, campaign_name = guess_client_and_campaign(filenames)
df["client_name"] = client_name
df["campaign_name"] = campaign_name

gerar_relatorio(
    df_list=dfList,
    template_md="template copy.md",
    client_name=client_name,
    campaign_name=campaign_name,
)

print("\n🎉 Relatório gerado com sucesso!")
