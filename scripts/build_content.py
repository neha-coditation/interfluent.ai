#!/usr/bin/env python3
"""Generate static content pages from Git-managed JSON entries (stdlib only)."""
import json, html, re, pathlib, shutil
from datetime import date
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"_site"
KINDS={"articles":("blog","Articles"),"case-studies":("case-studies","Case Studies")}
def esc(x): return html.escape(str(x),quote=True)
def slug(x):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",x): raise ValueError("Invalid slug: "+x)
    return x
def markdown(text):
    out=[]
    for line in text.splitlines():
        if line.startswith("## "):out.append("<h2>"+esc(line[3:])+"</h2>")
        elif line.startswith("# "):out.append("<h1>"+esc(line[2:])+"</h1>")
        elif line.strip():out.append("<p>"+esc(line)+"</p>")
    return "\n".join(out)
def page(title,body,description=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Interfluent</title><meta name="description" content="{esc(description)}"><link rel="stylesheet" href="/interfluent.ai/assets/css/global.css"><link rel="stylesheet" href="/interfluent.ai/assets/css/components.css"><style>main{{max-width:900px;margin:auto;padding:100px 24px 80px}}article{{line-height:1.7}}article h1{{font-size:clamp(2rem,5vw,3.5rem)}}.cms-card{{display:block;padding:24px;border:1px solid #ddd;border-radius:12px;margin:16px 0;color:inherit}}.cms-card:hover{{border-color:currentColor}}</style></head><body><main><nav><a href="/interfluent.ai/">Interfluent</a> / <a href="/interfluent.ai/blog/">Resources</a></nav>{body}</main></body></html>'''
def build():
    if OUT.exists():shutil.rmtree(OUT)
    shutil.copytree(ROOT,OUT,ignore=shutil.ignore_patterns(".git","_site","node_modules","__pycache__"))
    urls=[]
    for kind,(route,label) in KINDS.items():
        items=[]
        for file in sorted((ROOT/"content"/kind).glob("*.json")):
            obj=json.loads(file.read_text(encoding="utf-8"))
            if obj.get("status")!="published":continue
            ident=slug(obj["slug"]);items.append(obj)
            dest=OUT/route/ident/"index.html";dest.parent.mkdir(parents=True,exist_ok=True)
            content=f'<article><p>{esc(obj.get("category",label))} · {esc(obj.get("date",""))}</p><h1>{esc(obj["title"])}</h1><p>{esc(obj.get("description",""))}</p>{markdown(obj.get("body",""))}</article>'
            dest.write_text(page(obj["title"],content,obj.get("description","")),encoding="utf-8")
            urls.append(f"https://neha-coditation.github.io/interfluent.ai/{route}/{ident}/")
        if items and kind=="articles":
            # Keep the designed Blog page and append published CMS cards
            # with links to their own article detail pages.
            listing=OUT/"blog"/"index.html"
            if listing.exists():
                markup=listing.read_text(encoding="utf-8")
                start=markup.find('</main>')
                end=start
                if start!=-1:
                    cards_html="".join(
                        '<a class="blog_blog-posts_a" href="blog/'+esc(slug(o["slug"]))+'/">'
                        '<div class="blog_blog-posts_div-3">'+esc(o.get("category","ARTICLE"))+'</div>'
                        '<div class="blog_blog-posts_div-4">'+esc(o["title"])+'</div>'
                        '<p class="blog_blog-posts_p">'+esc(o.get("description",""))+'</p>'
                        '<div class="blog_blog-posts_div-5">'+esc(o.get("date",""))+'</div></a>'
                        for o in sorted(items,key=lambda x:x.get("date",""),reverse=True))
                    section='<section class="blog_blog-posts_section"><div class="blog_blog-posts_div">'+cards_html+'</div></section>\n'
                    markup=markup[:start]+section+markup[end:]
                    listing.write_text(markup,encoding="utf-8")
        if items and kind!="articles":
            cards="".join(f'<a class="cms-card" href="{esc(slug(o["slug"]))}/"><h2>{esc(o["title"])}</h2><p>{esc(o.get("description",""))}</p></a>' for o in sorted(items,key=lambda x:x.get("date",""),reverse=True))
            target=OUT/route/"index.html"
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(page(label,f"<h1>{esc(label)}</h1>"+cards),encoding="utf-8")
    (OUT/"cms-sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{esc(u)}</loc></url>" for u in urls)+"</urlset>",encoding="utf-8")
if __name__=="__main__":build()
