import os
import markdown
import pdfkit
from jinja2 import Environment, FileSystemLoader


# === CONFIGURAÇÃO DO WKHTMLTOPDF NO WINDOWS ===
# Ajuste o caminho abaixo se o seu estiver diferente
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


def carregar_template(nome_template: str):
    """Carrega o template .md usando Jinja2."""
    env = Environment(
        loader=FileSystemLoader('.'),  # pasta atual
        autoescape=False
    )
    return env.get_template(nome_template)


def preencher_markdown(dados: dict, nome_template: str, saida_md: str):
    """Renderiza o markdown substituindo os placeholders."""
    template = carregar_template(nome_template)
    conteudo = template.render(dados)

    with open(saida_md, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return saida_md


def converter_md_para_pdf(arquivo_md: str, arquivo_pdf: str):
    """Converte um arquivo .md para .pdf usando markdown + pdfkit (wkhtmltopdf)."""
    # 1) markdown → HTML
    with open(arquivo_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown.markdown(md_text)

    # 2) HTML → PDF usando wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

    # opções básicas (pode ajustar page-size, margins, etc.)
    options = {
        "page-size": "A4",
        "margin-top": "10mm",
        "margin-right": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
        "encoding": "UTF-8",
    }

    pdfkit.from_string(html, arquivo_pdf, configuration=config, options=options)

    return arquivo_pdf


def gerar_relatorio(dados: dict, template_md: str):
    """Pipeline completo: template .md → .md preenchido → PDF final."""
    artista_slug = dados.get("artist_name", "relatorio").replace(" ", "_")

    arquivo_md = f"{artista_slug}.md"
    arquivo_pdf = f"{artista_slug}.pdf"

    print(f"🔧 Preenchendo template → {arquivo_md}")
    preencher_markdown(dados, template_md, arquivo_md)

    print(f"📄 Convertendo .md → PDF → {arquivo_pdf}")
    converter_md_para_pdf(arquivo_md, arquivo_pdf)

    print("🎉 Relatório gerado com sucesso!")
    print(f"MD  👉 {os.path.abspath(arquivo_md)}")
    print(f"PDF 👉 {os.path.abspath(arquivo_pdf)}")


if __name__ == "__main__":
    # EXEMPLO DE DADOS – aqui você liga com o que puxar do CSV/API
    dados = {
        "artist_name": "teste1",
  "stats_period": "teste2",

  "ig_followers_start": "teste3",
  "ig_followers_end": "teste4",
  "fb_followers_start": "teste5",
  "fb_followers_end": "teste6",
  "spotify_listeners_start": "teste7",
  "spotify_listeners_end": "teste8",
  "yt_subs_start": "",
  "yt_subs_end": "",
  "yt_total_views": "",
  "twitter_followers_start": "",
  "twitter_followers_end": "",

  "illusions_total_spend": "",
  "release_day_boosts": "",

  "fb_boost_spend": "",
  "fb_boost_results": "",
  "fb_boost_cpc": "",
  "fb_boost_impressions": "",
  "fb_boost_reach": "",
  "fb_boost_video_plays": "",

  "ig_boost_spend": "",
  "ig_boost_results": "",
  "ig_boost_cpc": "",
  "ig_boost_impressions": "",
  "ig_boost_reach": "",
  "ig_boost_video_plays": "",

  "ep_lp_fb_spend": "",
  "ep_lp_fb_results": "",
  "ep_lp_fb_cpc": "",
  "ep_lp_fb_impressions": "",
  "ep_lp_fb_reach": "",

  "ep_lp_ig_spend": "",
  "ep_lp_ig_results": "",
  "ep_lp_ig_cpc": "",
  "ep_lp_ig_impressions": "",
  "ep_lp_ig_reach": "",

  "ep_spotify_ig_spend": "",
  "ep_spotify_ig_results": "",
  "ep_spotify_ig_cpc": "",
  "ep_spotify_ig_impressions": "",
  "ep_spotify_ig_reach": "",

  "ep_remarketing_spend": "",
  "ep_remarketing_results": "",
  "ep_remarketing_cpc": "",
  "ep_remarketing_impressions": "",
  "ep_remarketing_reach": "",

  "lr_ig_spend": "",
  "lr_ig_results": "",
  "lr_ig_cpc": "",
  "lr_ig_impressions": "",
  "lr_ig_reach": "",

  "mastermind_ig_spend": "",
  "mastermind_ig_results": "",
  "mastermind_ig_cpc": "",
  "mastermind_ig_impressions": "",
  "mastermind_ig_reach": "",

  "iywa_ig_spend": "",
  "iywa_ig_results": "",
  "iywa_ig_cpc": "",
  "iywa_ig_impressions": "",
  "iywa_ig_reach": "",

  "hero_ig_spend": "",
  "hero_ig_results": "",
  "hero_ig_cpc": "",
  "hero_ig_impressions": "",
  "hero_ig_reach": "",

  "hero_fb_spend": "",
  "hero_fb_results": "",
  "hero_fb_cpc": "",
  "hero_fb_impressions": "",
  "hero_fb_reach": "",

  "addicted_ig_spend": "",
  "addicted_ig_results": "",
  "addicted_ig_cpc": "",
  "addicted_ig_impressions": "",
  "addicted_ig_reach": "",

  "dontleave_ig_spend": "",
  "dontleave_ig_results": "",
  "dontleave_ig_cpc": "",
  "dontleave_ig_impressions": "",
  "dontleave_ig_reach": "",

  "yt_total_spend": "",

  "yt_hero_spend": "",
  "yt_hero_views": "",
  "yt_hero_cpv": "",
  "yt_hero_impressions": "",
  "yt_hero_engagements": "",
  "yt_hero_clicks": "",

  "yt_mastermind_spend": "",
  "yt_mastermind_views": "",
  "yt_mastermind_cpv": "",
  "yt_mastermind_impressions": "",
  "yt_mastermind_engagements": "",
  "yt_mastermind_clicks": "",

  "yt_lr_spend": "",
  "yt_lr_views": "",
  "yt_lr_cpv": "",
  "yt_lr_impressions": "",
  "yt_lr_engagements": "",
  "yt_lr_clicks": "",

  "yt_iywa_spend": "",
  "yt_iywa_views": "",
  "yt_iywa_cpv": "",
  "yt_iywa_impressions": "",
  "yt_iywa_engagements": "",
  "yt_iywa_clicks": "",

  "yt_discovery_spend": "",
  "yt_discovery_impressions": "",
  "yt_discovery_cpc": "",
  "yt_discovery_engagements": "",
  "yt_discovery_clicks": "",

  "spotify_audio_total_spend": "",

  "spotify1_spend": "",
  "spotify1_impressions": "",
  "spotify1_reach": "",
  "spotify1_intent_rate": "",
  "spotify1_new_listeners": "",

  "spotify2_spend": "",
  "spotify2_impressions": "",
  "spotify2_reach": "",
  "spotify2_intent_rate": "",
  "spotify2_new_listeners": "",

  "best_video_ep_album_trailer": "",
  "best_video_little_red": "",
  "best_video_mastermind": "",
  "best_video_iywa": "",
  "best_video_playlist_hero": "",
  "best_video_addicted": "",
  "best_video_dont_leave": "",

  "analyst_comments": ""
    }

    # Nome do template .md (aquele que montamos com os placeholders)
# TEMPLATE_MD = "template.md"

# gerar_relatorio(dados, TEMPLATE_MD)