# System Architecture: Codebrains.co.in

This repository uses **Astro** (Static Site Generator) built with a focus on fast content delivery, MDX for blog posts, and legacy static HTML layouts adapted into reusable Astro components.

## Core Directories

1. **`src/pages/`**: The routing engine
   - Contains structural pages: `index.astro` (Homepage), `contactus.astro`, `projects.astro`, `recommendation-engine.astro`.
   - Contains dynamic logic:
     - `blogs/[...page].astro`: The main paginated blog list (Page size: 9).
     - `blog/[...slug].astro`: The single blog post renderer mapped from Content Collections.

2. **`src/content/blog/`**: Content Collections (MDX & Markdown)
   - Astro Content Collections are strictly typed in `src/content.config.ts`.
   - **Frontmatter requirement**: All posts must have `title`, `date`, `description`, `tags`, `series`, and `seriesLabel`. `heroImage` and `ogImage` are optional image paths.
   - Do NOT use the `layout:` property in MDX frontmatter, as the `blog/[...slug].astro` dynamic route already wraps output in the `BlogPostLayout.astro`. Using it causes duplicate headers and social icons.

3. **`src/layouts/`**: Core UI wrappers
   - `BaseLayout.astro`: Contains the `<html>`, `<head>`, global `<nav>`, `<header>`, and social share icons.
   - `BlogPostLayout.astro`: Inherits `BaseLayout`, injects a conditional hero image (`{frontmatter.heroImage && ...}`), and sets up the `<article class="blog-post">` container.

4. **`public/`**: Static Assets
   - Images and resources go here. Astro copies this entire folder into `dist/` unconditionally during build.
   - **Critical**: `public/CNAME` must exist to preserve the `codebrains.co.in` custom domain during GitHub Pages action deployments.

## Styling
- Styling relies primarily on standard CSS and older Bootstrap class patterns (`container`, `row`, `col-lg-5`, etc.).
- Custom styling is injected via `BaseLayout` (`resources/assets/css/blog.css`, etc.).
- There is no TailwindCSS in this project. Stick to vanilla CSS and existing class structures.
