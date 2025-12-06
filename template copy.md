# {{ client_name }} – AD REPORT

## Social / Streaming Stats
- **Instagram Followers:** {{ ig_followers_start }} → {{ ig_followers_end }}
- **Facebook Followers:** {{ fb_followers_start }} → {{ fb_followers_end }}
- **Spotify Monthly Listeners:** {{ spotify_listeners_start }} → {{ spotify_listeners_end }}
- **YouTube Subscribers:** {{ yt_subs_start }} → {{ yt_subs_end }}
  - **Total Video Views:** {{ yt_total_views }}
- **Twitter Followers:** {{ twitter_followers_start }} → {{ twitter_followers_end }}

---

# {{ campaign_name }}

# ADVERTISING REPORTS

{% for plataforma in platforms %}
## {{ plataforma.platform_name }}

{% for post in plataforma.posts %}
{% set ad_name = post.get("Ad name") or post.get("Video") or "Unnamed Ad" %}

### {{ ad_name }}

{% for chave, valor in post.items() %}
{% if chave not in ["Ad name", "Video"] %}
- **{{ chave }}:** {{ valor }}
{% endif %}
{% endfor %}

---

{% endfor %}
{% endfor %}
