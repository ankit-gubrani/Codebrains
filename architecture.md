# Architecture: codebrains.co.in (Astro Migration)

## Overview

The website has been migrated from **hand-authored static HTML** to **Astro v6** as the Static Site Generator. Astro pre-renders every page at build time into optimized static HTML, CSS, and JS — no server runtime needed.

---

## Directory Structure

```
├── astro.config.mjs          # Astro config (MDX, Sitemap, build format)
├── src/
│   ├── content.config.ts     # Blog collection schema (Astro 5+ loader API)
│   ├── content/blog/         # MDX blog posts (content collection)
│   │   ├── 2025/ai/          # 8 posts — converted to .mdx
│   │   ├── 2026/ai/          # 9 posts — converted to .mdx
│   │   └── posts/            # 3 legacy AEM posts — converted to .mdx
│   ├── assets/img/           # Optimized images (processed by Astro Image)
│   ├── layouts/
│   │   ├── BaseLayout.astro  # Shared shell: <head>, nav, footer, GA, MailChimp
│   │   └── BlogPostLayout.astro  # Wraps BaseLayout + injects JSON-LD schema
│   └── pages/
│       ├── index.astro       # Homepage
│       ├── blogs/[...page].astro     # Paginated blog index
│       ├── blog/[...slug].astro      # Dynamic single-post route
│       ├── blog/[series]/[...page].astro  # Series index with pagination
│       ├── deck/*.astro      # Presentation decks (reveal.js)
│       ├── projects/*.astro  # Project showcase pages
│       └── *.astro           # About, Contact, etc.
├── public/resources/         # Static assets served as-is (CSS, JS, fonts)
├── dist/                     # Build output (deploy this folder)
├── generate_blog.py          # Automation script: blog.json → MDX
└── generate_blog_using_astro.md  # How-to guide for publishing new posts
```

---

## Key Design Decisions

### 1. Astro Content Collections (v5+ Loader API)
- Blog posts are defined as a **content collection** in `src/content.config.ts` using the `glob` loader pattern matching `**/*.{md,mdx}`.
- All posts have been migrated to `.mdx` to support inline HTML/SVGs and stricter character escaping.
- Schema validates: `title`, `date`, `description`, `ogImage`, `tags`, `series`, `seriesLabel`, `part`, `canonicalUrl`.
- Posts are queried via `getCollection('blog')` and rendered with `render(post)`.

### 2. URL Preservation
- `build.format: 'file'` ensures URLs like `/blog/2025/ai/what-is-rag` produce `dist/blog/2025/ai/what-is-rag.html` — matching the old site exactly.
- `trailingSlash: 'never'` prevents trailing-slash redirects.

### 3. SEO: JSON-LD Article Schema
- `BlogPostLayout.astro` injects a `<script type="application/ld+json">` block with Article schema fields (headline, author, publisher, datePublished, image, etc.) derived from frontmatter.

### 4. Image Optimization
- Blog images live in `src/assets/img/` so Astro's built-in image pipeline converts them to **WebP** with `loading="lazy"` and `decoding="async"`.
- Build stats: images like `prompt_caching-intro.png` (1549 kB) → optimized WebP (101 kB).

### 5. Sitemap
- `@astrojs/sitemap` auto-generates `sitemap-index.xml` + `sitemap-0.xml` on every build — no manual maintenance.

### 6. Static Pages
- The original HTML templates for decks (reveal.js), projects, and core pages are wrapped inside `BaseLayout` as `.astro` pages.
- JavaScript `{}` in inline code blocks are escaped as `&#123;`/`&#125;` to avoid Astro JSX parsing.

---

## Migration Summary

| What | Count |
|---|---|
| Blog posts migrated | 20 (17 AI + 3 legacy AEM) |
| Static pages migrated | 14 (index, about, contact, projects, decks) |
| Total pages generated | 39 |
| Images optimized | 41 |
| Sitemap URLs | 39 |

---

## Gotchas & Lessons Learned

### Astro 5+ Breaking Changes
- **Content config location**: Must be `src/content.config.ts` (not `src/content/config.ts`). The old path throws `LegacyContentConfigError`.
- **Collection API**: `post.slug` → `post.id`, and `post.render()` → `render(post)` (imported from `astro:content`).
- **Loader required**: Collections must declare a `loader` (e.g., `glob()`); the legacy implicit behavior is removed.

### MDX & JSX Escaping
- **MDX Conversion**: All blog posts were converted to `.mdx` because standard Markdown sanitizes inline SVGs. MDX allows raw HTML/SVG but is stricter about JSX syntax.
- **Curly braces** `{` `}` inside `.mdx` and `.astro` files are treated as JSX expressions. They must be escaped as `&#123;` / `&#125;` if they are literals (e.g., in code snippets or SVG styles).
- **"Less than" signs** `<` followed by a number (e.g., `< 0.65`) or space can break the MDX parser. These are escaped as `&lt;`.
- **HTML Comments** `<!-- -->` fail in MDX. They must be converted to MDX comments `{/* ... */}`.
- **Script tags** referencing files in `public/` must include `is:inline` to prevent Vite from trying to bundle them.

### SSL/TLS on Local Network
- The local dev environment had certificate issues. `NODE_TLS_REJECT_UNAUTHORIZED=0` was needed during initial `npm install` and `create-astro`.

### Python Publishing Script
- `generate_blog.py` outputs `.mdx` files with YAML frontmatter.
- It automatically handles MDX-specific escaping: converting HTML comments, escaping curly braces, and escaping non-tag angle brackets.

### Image Path Convention
- Images in `src/assets/img/` → Astro optimizes them (WebP, lazy loading).
- Images in `public/resources/` → served as-is (no optimization, use for external reference assets).

---

## Commands Reference

```bash
npm run dev       # Local dev server at localhost:4321
npm run build     # Production build → dist/
npm run preview   # Preview the built site locally
```
