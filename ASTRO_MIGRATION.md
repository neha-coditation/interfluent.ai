# Astro migration

This branch introduces Astro without deleting the existing static site.

## Local development

```bash
npm install
npm run dev
```

Production build:

```bash
npm run build
npm run preview
```

Astro writes the production site to `dist/`.

## Current structure

- `src/components/Navbar.astro` — shared navigation
- `src/components/Footer.astro` — shared footer
- `src/layouts/BaseLayout.astro` — shared document, SEO, favicon and layout shell
- `src/pages/index.astro` — first Astro route / migration preview
- `public/assets/` — copied from the current site's assets so the existing design system can be reused

## Migration strategy

The existing HTML/DC files remain in the repository as the visual and content source. Move pages one at a time into `src/pages/`, preserving current class names first. Once all routes are migrated and tested, the legacy files can be removed.

Do not deploy this branch to production until route parity has been checked.
