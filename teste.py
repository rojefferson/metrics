from typing import List, Tuple
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

filenames = [
    f for f in os.listdir(csvDir)
    if f.lower().endswith((".csv", ".xlsx"))
]

client_name, campaign_name = guess_client_and_campaign(filenames)

print(f"👤 Cliente: {client_name}")
print(f"📣 Campanha: {campaign_name}")
