from urllib.parse import urlparse, parse_qs

def youtube_embed(url: str) -> str:
    if not url:
        return ""
    u = urlparse(url)

    # youtu.be/VIDEOID
    if "youtu.be" in u.netloc:
        vid = u.path.lstrip("/")
    else:
        # youtube.com/watch?v=VIDEOID
        qs = parse_qs(u.query)
        vid = qs.get("v", [""])[0]

    if not vid:
        return ""

    # player mais estável + sem cookies
    return f"https://www.youtube-nocookie.com/embed/{vid}?rel=0"
