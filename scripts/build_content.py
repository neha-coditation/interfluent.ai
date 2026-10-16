#!/usr/bin/env python3
"""Build Git-managed content using the existing Interfluent page templates."""
import html
import json
import os
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
BASE = "/interfluent.ai/"
SITE = "https://neha-coditation.github.io" + BASE
KINDS = {"articles": ("blog", "Articles"), "case-studies": ("case-studies", "Case Studies")}

def esc(value):
    return html.escape(str(value or ""), quote=True)

def slug(value):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError("Invalid slug: " + value)
    return value

def richtext(value):
    result = []
    for paragraph in re.split(r"\n\s*\n", value or ""):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if paragraph.startswith("## "):
            result.append('<h2 class="blog-post_post_h2">' + esc(paragraph[3:]) + "</h2>")
        elif paragraph.startswith("# "):
            result.append('<h2 class="blog-post_post_h2">' + esc(paragraph[2:]) + "</h2>")
        else:
            result.append('<p class="blog-post_post_p-2">' + esc(paragraph).replace("\n", "<br>") + "</p>")
    return "\n".join(result)

def article_page(obj, template):
    image = obj.get("image", "")
    hero = ('<img class="blog-post_post_div-2" src="' + BASE + esc(image) +
            '" alt="' + esc(obj["title"]) + '" style="width:100%;object-fit:cover;display:block">' if image else "")
    body = (
        '<article data-screen-label="Post" class="blog-post_post_article is-first-section">'
        + '<a href="' + BASE + 'blog/" class="blog-post_post_a">← All posts</a>'
        + '<div class="blog-post_post_div">' + esc(obj.get("category", "ARTICLE")).upper() + ' · ' + esc(obj.get("date", "")) + '</div>'
        + '<h1 class="blog-post_post_h1">' + esc(obj["title"]) + '</h1>'
        + '<p class="blog-post_post_p">' + esc(obj.get("description", "")) + '</p>'
        + hero
        + '<div class="blog-post_post_div-3">' + richtext(obj.get("body", "")) + '</div>'
        + '<div class="blog-post_post_div-4"><div class="blog-post_post_div-5">Written by ' + esc(obj.get("author", "Interfluent team"))
        + '.</div><a href="' + BASE + 'blog/" class="blog-post_post_a-3">More posts →</a></div></article>'
    )
    start = template.index('<article data-screen-label="Post"')
    end = template.index('</article>', start) + len('</article>')
    page = template[:start] + body + template[end:]
    page = page.replace('<html data-seo-page="blog-post">', '<html lang="en" data-seo-page="blog-post">', 1)
    meta = ('<title>' + esc(obj["title"]) + ' | Interfluent</title>'
            '<meta name="description" content="' + esc(obj.get("description", "")) + '">'
            '<link rel="canonical" href="' + SITE + 'blog/' + slug(obj["slug"]) + '/">')
    if image:
        meta += '<meta property="og:image" content="' + SITE + esc(image) + '">'
    return page.replace('</head>', meta + '\n</head>', 1)

def generic_page(obj):
    image = obj.get("image", "")
    image_tag = '<img src="' + BASE + esc(image) + '" alt="' + esc(obj["title"]) + '" style="max-width:100%">' if image else ""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1"><title>' + esc(obj["title"]) + ' | Interfluent</title>'
            '<link rel="stylesheet" href="' + BASE + 'assets/css/global.css"></head><body>'
            '<main style="max-width:780px;margin:80px auto;padding:24px"><a href="' + BASE + '">Interfluent</a>'
            '<h1>' + esc(obj["title"]) + '</h1>' + image_tag + richtext(obj.get("body", "")) + '</main></body></html>')

def seo_tags(title, description, url, image=None, kind="website"):
    title, description = esc(title), esc(description)
    image_url = SITE + (image or "assets/images/og/interfluent-og.svg").lstrip("/")
    return ("<title>" + title + "</title>\n"
            + '<meta name="description" content="' + description + '">\n'
            + '<link rel="canonical" href="' + esc(url) + '">\n'
            + '<meta property="og:type" content="' + kind + '">\n'
            + '<meta property="og:site_name" content="Interfluent">\n'
            + '<meta property="og:title" content="' + title + '">\n'
            + '<meta property="og:description" content="' + description + '">\n'
            + '<meta property="og:url" content="' + esc(url) + '">\n'
            + '<meta property="og:image" content="' + esc(image_url) + '">\n'
            + '<meta name="twitter:card" content="summary_large_image">\n'
            + '<meta name="twitter:title" content="' + title + '">\n'
            + '<meta name="twitter:description" content="' + description + '">\n'
            + '<meta name="twitter:image" content="' + esc(image_url) + '">\n')

def set_seo(page, title, description, url, image=None, kind="website"):
    # Remove any stale, duplicate metadata before inserting canonical SEO values.
    page = re.sub(r'<title[^>]*>.*?</title>', '', page, flags=re.I | re.S)
    page = re.sub(r'<meta\\s+(?:name|property)="(?:description|robots|og:[^"]+|twitter:[^"]+)"[^>]*>', '', page, flags=re.I)
    page = re.sub(r'<link\\s+rel="canonical"[^>]*>', '', page, flags=re.I)
    return page.replace("</head>", seo_tags(title, description, url, image, kind) + "</head>", 1)

def apply_site_seo():
    # The repository uses seo-config.js as the central metadata registry.
    config_source = (ROOT / "assets/js/seo-config.js").read_text(encoding="utf-8")
    match = re.search(r'pages:\s*\{', config_source)
    if not match:
        raise ValueError("Missing SEO page registry")
    # Parse the page registry via a limited key/value pattern; descriptions are plain strings.
    records = {}
    pattern = r'(?:"([^"]+)"|([a-zA-Z-]+)):\s*\{\s*path:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*description:\s*"([^"]+)"'
    for m in re.finditer(pattern, config_source):
        key = m.group(1) or m.group(2)
        records[key] = dict(path=m.group(3), title=m.group(4), description=m.group(5))
    for file in OUT.rglob("index.html"):
        if "_site" in file.relative_to(OUT).parts:
            continue
        relative = file.relative_to(OUT)
        route = "/" if relative.as_posix() == "index.html" else "/" + relative.parent.as_posix() + "/"
        markup = file.read_text(encoding="utf-8")
        page_match = re.search(r'<html[^>]*data-seo-page="([^"]+)"', markup)
        key = page_match.group(1) if page_match else None
        # CMS detail pages are populated directly from their JSON records.
        if route.startswith("/blog/") and route != "/blog/" and route != "/blog/everyone-ships-fast-now/":
            source = ROOT / "content/articles" / (relative.parent.name + ".json")
        elif route.startswith("/case-studies/") and route != "/case-studies/":
            source = ROOT / "content/case-studies" / (relative.parent.name + ".json")
        else:
            source = None
        if source and source.exists():
            record = json.loads(source.read_text(encoding="utf-8"))
            title = record["title"] + " | Interfluent"
            desc = record.get("description", "")
            image = record.get("image")
            kind = "article"
        elif route == "/blog/everyone-ships-fast-now/":
            title = "Everyone ships fast now. Together, you still don't. | Interfluent"
            desc = "AI made each function faster on its own. Explore why cross-functional shipping needs shared context."
            image = "assets/images/blog/everyone-ships-fast-now.svg"
            kind = "article"
        elif key in records:
            title = records[key]["title"]
            desc = records[key]["description"]
            image = None
            kind = "website"
        else:
            continue
        markup = set_seo(markup, title, desc, SITE.rstrip("/") + route, image, kind)
        file.write_text(markup, encoding="utf-8")

def normalize_cloudflare_paths():
    """Pages is hosted at the domain root; GitHub Pages uses /interfluent.ai/."""
    if not os.environ.get("CF_PAGES"):
        return
    for file in OUT.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in {".html", ".css", ".js", ".xml", ".json"}:
            continue
        content = file.read_text(encoding="utf-8")
        updated = content.replace("https://neha-coditation.github.io/interfluent.ai/", "https://interfluent-ai.pages.dev/")
        updated = updated.replace("/interfluent.ai/", "/")
        # The legacy prefix also appears without a trailing slash in some links.
        updated = updated.replace('href="/interfluent.ai"', 'href="/"')
        if updated != content:
            file.write_text(updated, encoding="utf-8")


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT, OUT, ignore=shutil.ignore_patterns(".git", "_site", "node_modules", "__pycache__"))
    blog_template = (ROOT / "blog/everyone-ships-fast-now/index.html").read_text(encoding="utf-8")
    urls = []
    for kind, (route, label) in KINDS.items():
        items = []
        for file in sorted((ROOT / "content" / kind).glob("*.json")):
            obj = json.loads(file.read_text(encoding="utf-8"))
            if obj.get("status") != "published":
                continue
            ident = slug(obj["slug"])
            items.append(obj)
            dest = OUT / route / ident / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Rebuild every CMS page from one shared template; never maintain per-post HTML.
            if kind == "articles":
                dest.write_text(article_page(obj, blog_template), encoding="utf-8")
            else:
                # Preserve designed case study pages; use shared article layout for new records.
                if not dest.exists():
                    case_template = blog_template.replace('href="/interfluent.ai/blog/"', 'href="/interfluent.ai/case-studies/"')
                    case_obj = dict(obj)
                    case_obj["category"] = obj.get("category", "Case Study") + " · Illustrative scenario"
                    dest.write_text(article_page(case_obj, case_template).replace("← All posts", "← All case studies").replace("More posts →", "More case studies →"), encoding="utf-8")
            urls.append(SITE + route + "/" + ident + "/")
        if kind == "articles":
            listing = OUT / "blog/index.html"
            markup = listing.read_text(encoding="utf-8")
            cards = "".join(
                '<a class="blog_blog-posts_a" href="' + BASE + 'blog/' + slug(o["slug"]) + '/">'
                + ('<img src="' + BASE + esc(o["image"]) + '" alt="" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px">' if o.get("image") else "")
                + '<div class="blog_blog-posts_div-3">' + esc(o.get("category", "ARTICLE")) + '</div>'
                + '<div class="blog_blog-posts_div-4">' + esc(o["title"]) + '</div>'
                + '<p class="blog_blog-posts_p">' + esc(o.get("description", "")) + '</p>'
                + '<div class="blog_blog-posts_div-5">' + esc(o.get("date", "")) + '</div></a>'
                for o in sorted(items, key=lambda item: item.get("date", ""), reverse=True))
            section = '<section class="blog_blog-posts_section"><div class="blog_blog-posts_div">' + cards + '</div></section>\n'
            if "<!-- CMS BLOG POSTS START -->" in markup:
                markup = re.sub(
                    r"<!-- CMS BLOG POSTS START -->.*?<!-- CMS BLOG POSTS END -->",
                    lambda match: "<!-- CMS BLOG POSTS START -->" + section + "<!-- CMS BLOG POSTS END -->",
                    markup,
                    flags=re.S,
                )
            else:
                markup = markup.replace("</main>", "<!-- CMS BLOG POSTS START -->" + section + "<!-- CMS BLOG POSTS END --></main>", 1)
            listing.write_text(markup, encoding="utf-8")
        elif items:
            # Keep the designed listing and shared navigation/footer.
            listing = OUT / route / "index.html"
            if not listing.exists():
                raise FileNotFoundError("Case studies listing template missing")
    apply_site_seo()
    (OUT / "cms-sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join("<url><loc>" + esc(url) + "</loc></url>" for url in urls) + "</urlset>", encoding="utf-8")
    normalize_cloudflare_paths()
    if os.environ.get("CF_PAGES"):
        # Preserve old prefixed URLs with permanent redirects on Cloudflare Pages.
        (OUT / "_redirects").write_text(
            "/interfluent.ai / 301\\n"
            "/interfluent.ai/ / 301\\n"
            "/interfluent.ai/* /:splat 301\\n",
            encoding="utf-8",
        )

if __name__ == "__main__":
    build()
