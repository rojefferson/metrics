import pandas as pd
import os

currentDir = os.path.dirname(os.path.abspath(__file__))
parentDir = os.path.dirname(currentDir)
csvDir = os.path.join(parentDir, "source")


colsMeta = [
    "Clicks (all)",
    "Link clicks",
    "CTR (link click-through rate)",
    "CPC (all) (USD)",
    "Page engagement",
    "Views",
    "3-second video plays"
]

colsGoogle = [
    "Clicks"
    "CTR",
    "Engagements",
    "Engagement rate",
    "Watch time (hrs)",
    "Average watch time",
    "Video played to %"
]

colsTiktok = [
    "Clicks (all)",
    "CTR (all)",
    "CPC (destination)",
    "Video views",
    "Video view rate",
    "Average watch time"
]

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
    elif "GOOGLE" in file.upper():
        cols = colsGoogle
        source = "Google"
        encoding = "utf-16"
        skiprows = 2
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
            sep="\t"
        )

        # cols_to_use = [c for c in cols if c in header_df.replace("'", "").replace(" ", "").split(",")]

        df = pd.read_csv(full_path, encoding=encoding ,sep="\t" ,header=skiprows)
        df.columns = df.columns.str.strip()               # remove espaços
        df.columns = df.columns.str.replace('\ufeff','')  # remove BOM invisível
        df.columns = df.columns.str.replace('\u200b','')  # remove espaço zero-width
        df.columns = df.columns.str.replace('\n','')      # remove quebras
        df.columns = df.columns.str.replace('\r','')
        drop_cols = [c for c in cols if c not in header_df.columns]
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
