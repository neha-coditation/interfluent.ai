# Interfluent Website

Astro-based marketing site for Interfluent.

## Development

Requirements:
- Node.js 22.12+
- npm

Install dependencies and run locally:

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
npm run preview
```

Astro outputs the static production site to `dist/`.

## Project structure

```text
src/
├── components/
│   ├── Navbar.astro
│   ├── Footer.astro
│   └── HomePage.astro
├── layouts/
│   └── BaseLayout.astro
├── pages/
│   ├── index.astro
│   ├── about.astro
│   ├── pricing.astro
│   ├── contact.astro
│   ├── careers.astro
│   ├── privacy.astro
│   ├── signin.astro
│   ├── beta.astro
│   ├── terms.astro
│   └── blog/
│       ├── index.astro
│       └── [slug].astro
├── content/
│   └── blog/
└── config/
    └── site.ts

public/
└── assets/
    ├── css/
    └── images/
```

## Blog CMS-like workflow

Add a Markdown file under:

```text
src/content/blog/
```

Example:

```md
---
title: "New blog title"
description: "Short description"
publishDate: 2026-10-06
author: "Interfluent team"
category: "Product"
readTime: "5 min"
featured: false
---

Article content.
```

The blog listing and individual `/blog/<slug>/` page are generated automatically.

## Hosting

The project builds to static files, so it can be deployed to AWS S3 + CloudFront, Cloudflare, or another static host.

The current migration work is on the `astro-migration` branch.
