
# Relatório da campanha

**Cliente:** {{ client_name }}
**Campanha:** {{ campaign_name }}

---

{% for plataforma in platforms %}

## 📌 Plataforma:}

{% if plataforma.posts|length == 0 %}

> Nenhum post encontrado nesta plataforma.

{% else %}

{% for post in plataforma.posts %}

### 🔹 Post / Vídeo:

{% if post.get("Ad name") %}**{{ post["Ad name"] }}**{% endif %}
{% if post.get("Video") %}**{{ post["Video"] }}**{% endif %}

| Métrica                                   | Valor       |
| ------------------------------------------ | ----------- |
| {% for chave, valor in post.items() %}     |             |
| {% if chave not in ["Ad name", "Video"] %} |             |
| **{{ chave }}**                      | {{ valor }} |
| {% endif %}                                |             |
| {% endfor %}                               |             |

---

{% endfor %}
{% endif %}

---

{% endfor %}
