# Interfluent Git-based content CMS

Articles live in `content/articles/`; case studies in `content/case-studies/`.

To create content, copy an existing JSON file, change `title`, `slug`, `date`, `description`, and `body`. Use `status: "draft"` to keep it private from the published website, and `status: "published"` to include it in the next deployment. Draft files are still public in a public GitHub repository, so don't put confidential drafts there.

The build creates `/blog/<slug>/` and `/case-studies/<slug>/`, listing pages when published entries exist, and `/cms-sitemap.xml`.

Enable **Settings → Pages → Build and deployment → Source: GitHub Actions** before using the workflow. If the repository already has another Pages deployment workflow, disable the older one to prevent conflicting deployments.

Run locally with `python3 scripts/build_content.py`. No additional packages are required.

This is a first-stage Git-managed CMS, not yet a Webflow-like visual editor. Publishing is by editing JSON and committing; existing page design and CMS templates should be integrated and QA'd before production deployment.
