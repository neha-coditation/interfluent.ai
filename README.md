# Interfluent / CodeLens Website

Static GitHub-ready build created from the supplied `Landing_Page_Responsive.zip` export.

## Live reference

The current Webflow implementation remains the visual/content reference:

- https://interfluent.webflow.io/

## Main pages

- `index.html` — current landing page (based on the supplied **CodeLens Landing v1** export, which most closely matches the live Webflow homepage)
- `about.html`
- `pricing.html`
- `blog.html`
- `blog-post.html`
- `careers.html`
- `contact.html`
- `beta.html`
- `signin.html`
- `privacy.html`
- `terms.html`

## Design/prototype pages

- `landing-original.html`
- `landing-diagrammatic.html`
- `landing-kinetic.html`
- `hero-sketches.html`

## Shared files

- `SiteNav.dc.html` — shared navigation component
- `SiteFooter.dc.html` — shared footer component
- `responsive.css` — responsive layout rules
- `site-config.js` — site-wide switches and landing route
- `support.js` — runtime required by the exported Design Components and scroll interactions
- `uploads/` — supplied PDF references
- `source/` — untouched unpacked `.dc.html` source exports for reference

## Run locally

Because the pages load shared components with `fetch()`, serve the folder over HTTP rather than opening `index.html` directly from Finder.

```bash
python3 -m http.server 3000
```

Then open `http://localhost:3000/`.

## GitHub Pages

This repository is ready for GitHub Pages. In GitHub, choose **Settings → Pages → Deploy from a branch**, then select the `main` branch and `/ (root)`.

## Notes

The supplied pages are exported Design Components rather than conventional standalone HTML. The repository keeps their runtime so the interactive/scroll-driven sections continue to work, while exposing normal public filenames such as `about.html`, `careers.html`, and `contact.html`.
