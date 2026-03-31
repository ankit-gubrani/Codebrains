# PRD: Introduce Astro to codebrains.co.in on GitHub Pages

**Author:** Ankit Gubrani  
**Status:** Draft  
**Last Updated:** March 2026

---

## 1. Background

codebrains.co.in is a technical blog targeting engineers and architects building AI-powered systems. The site currently runs as fully static HTML hosted on GitHub Pages, with Cloudflare acting as the CDN layer in front of it. All pages are hand-authored HTML files with headers, footers, and nav duplicated across every file. New blog posts are generated via a Python script that takes an LLM-generated JSON object and outputs a complete HTML file.

The site has grown to 20+ blog posts across multiple series, plus additional standalone pages covering projects, presentations, and profile content. The current setup is showing its limits: any global layout change requires touching every file, there is no pagination on the blog listing or series index pages, and the Python publishing script is producing increasingly large HTML blobs instead of focusing on content.

---

## 2. Full Site Page Inventory

The following is the complete inventory of all pages on codebrains.co.in that must be migrated. Every URL listed here must resolve identically after migration with no redirects.

### Core Site Pages

| Page | URL | Type |
|---|---|---|
| Home | `/` | Static page |
| Blog listing | `/blogs` | Dynamic listing with pagination |
| About hub | `/ankitgubrani` | Static page |
| About me | `/about/ankitgubrani` | Static page |
| Follow me | `/followme` | Static page |
| Contact | `/contactus` | Static page |
| Our Work | `/projects` | Static page |

### Blog Series Index Pages

| Page | URL | Type |
|---|---|---|
| AI Building Blocks series | `/blog/ai-building-blocks-for-modern-web` | Dynamic series index with pagination |
| AI Radar series | `/blog/ai-radar` | Dynamic series index with pagination |

### Blog Posts - AI Building Blocks Series (2025)

| Title | URL |
|---|---|
| RAG: The Missing Link Between your Data and AI That actually Works | `/blog/2025/ai/what-is-rag-retrieval-augmented-generation-guide` |
| RAG vs CAG vs KAG: Choosing the Right Augmentation Strategy | `/blog/2025/ai/rag-vs-cag-vs-kag-choosing-right-augmentation-strategy` |
| Vector Databases: The Search Engine Your RAG System Actually Needs | `/blog/2025/ai/vector-databases-search-engine-rag-system-actually-needs` |
| Model Context Protocol: The Universal Adapter Your AI Stack Actually Needs | `/blog/2025/ai/model-context-protocol-the-universal-adapter-your-ai-stack-actually-needs` |
| Context Rot: The Silent Performance Killer in Your RAG System | `/blog/2025/ai/context-rot-silent-performance-killer-in-your-rag-system` |
| Context Engineering: The Discipline Your AI System Desperately Needs | `/blog/2025/ai/context-engineering-the-discipline-your-ai-system-desperately-needs` |
| Semantic Cache: The Smartest Way to Speed Up RAG | `/blog/2025/ai/semantic-cache-smartest-way-to-speed-up-rag` |
| Corrective RAG: The Self-Healing Retrieval Layer | `/blog/2025/ai/corrective-rag-self-healing-retrieval-layer-your-rag-system-desperately-needs` |

### Blog Posts - AI Building Blocks Series (2026)

| Title | URL |
|---|---|
| Prompt Caching: The Secret to 10x Faster LLM Responses | `/blog/2026/ai/prompt-caching-the-secret-to-10x-faster-llm-responses` |
| PageIndex: The Reasoning-Based RAG Engine That Thinks Before It Retrieves | `/blog/2026/ai/pageIndex-reasoning-based-rag-engine-that-thinks-before-it-retrieves` |
| How LLMs Actually Think: Transformers and Attention Explained | `/blog/2026/ai/how-llms-actually-think-transformers-and-attention-explained` |
| When Attention Becomes a Bottleneck: How Mamba Is Rethinking Long-Context AI | `/blog/2026/ai/when-attention-becomes-bottleneck-how-mamba-is-rethinking-long-context-ai` |
| The Same Trick That Made Transformers Great Just Made Them Better | `/blog/2026/ai/same-trick-that-made-transformers-great-just-made-them-better` |

### Blog Posts - AI Radar Series (2026)

| Title | URL |
|---|---|
| MoltBot: The AI Agent That Could Be Your Personal Jarvis | `/blog/2026/ai/moltbot-the-ai-agent-that-could-be-your-personal-jarvis` |
| Moltbook: When Your AI Gets a Social Life | `/blog/2026/ai/moltbook-when-your-ai-gets-a-social-life` |
| When AEM Meets AI: How MCP is Turning Content Management into a Conversation | `/blog/2026/ai/when-aem-meets-ai-mcp-turning-content-management-into-conversation` |
| Repeat Yourself: How Prompt Repetition Quietly Boosts LLM Accuracy for Free | `/blog/2026/ai/repeat-yourself-how-prompt-repetition-quietly-boosts-llm-accuracy-for-free` |

### Legacy Blog Posts (Pre-Series, 2022)

These three posts live under a different URL structure (`/blog/posts/`) and have no series affiliation. They appear only on the main `/blogs` listing.

| Title | URL |
|---|---|
| Integrating Apache Wookie with AEM | `/blog/posts/integratingwookiewithAEM` |
| Creating Custom content finder tab in AEM | `/blog/posts/creatingCustomContentFinderTabAEM` |
| Configuring AEM 6.0 with mongoMK | `/blog/posts/configuringAEMwithMongoMK` |

### Project Pages

| Page | URL |
|---|---|
| AEM Recommendation Generator | `/recommendation-engine` |
| Offline WebPage Editor Chrome Extension | `/projects/offline-webpage-editor` |
| AEM-Mahout Connector | `/projects/aem-mahout-connector` |
| AEM-Wookie Connector | `/projects/aem-wookie-connector` |

### Presentation / Deck Pages

| Page | URL |
|---|---|
| Sling Pipes | `/deck/sling-pipes` |
| Circuit Breaker Pattern | `/deck/circuit-breaker-pattern` |
| Unit Testing and Mocking with Junit5 and AEM Mocks | `/deck/unit-testing-and-mocking` |

---

## 3. Problem Statement

The current architecture has four core problems:

**No templating.** The header, footer, navigation, and page chrome are duplicated in every HTML file across all page types. A single nav link change requires editing every page manually.

**No pagination.** The `/blogs` listing page and each series index page load all posts in one shot. As the post count grows, these pages become slow and hard to navigate.

**Publishing friction.** The Python script generates full HTML files including all boilerplate. This means any layout change also requires regenerating or patching every previously generated post file.

**No separation of content from presentation.** Content and structure are mixed together in every generated HTML file, making both harder to maintain independently.

---

## 4. Goals

- Eliminate all duplicated header/footer/nav HTML across all page types
- Enable independent pagination on the main blog listing and on each series index page
- Simplify the Python publishing script so it only generates content (Markdown + YAML front matter), not full HTML
- Migrate every page listed in Section 2 to the Astro build system
- Maintain zero hosting cost
- Preserve all existing URLs exactly to protect SEO
- Keep the site fully static at build time
- Make no changes to the existing Cloudflare CDN setup or DNS configuration

---

## 5. Non-Goals

- No change to hosting provider: GitHub Pages remains the origin
- No change to the Cloudflare CDN layer or DNS configuration
- No dynamic server-side features at launch (comments, search, auth)
- No visual redesign; existing CSS and layout must be preserved exactly across all page types
- No migration away from GitHub as the source of truth for content

---

## 6. Proposed Solution

Introduce **Astro** as the static site generator into the existing GitHub repository. A **GitHub Actions** workflow runs `astro build` on every push to `main` and deploys the output to the `gh-pages` branch. GitHub Pages continues to serve the site exactly as before. Cloudflare CDN sits in front and requires zero reconfiguration.

### 6.1 Why Astro

Astro is a static site generator with a component model and native content collections. It produces zero-JS HTML by default, matching the existing site's fully static nature. Its `paginate()` helper works across any collection independently. The component model replaces the duplicated header/footer pattern with a single shared layout file that applies across all page types.

### 6.2 Why Stay on GitHub Pages

The site already uses Cloudflare as its CDN in front of GitHub Pages. The primary performance benefit of alternative hosts is already present. Staying on GitHub Pages avoids DNS changes, eliminates cutover risk, and keeps the entire stack on infrastructure that has been running reliably since the site launched.

### 6.3 How the Build Pipeline Works

```
Push to main
  -> GitHub Actions triggers
  -> npm install && astro build
  -> dist/ pushed to gh-pages branch
  -> GitHub Pages serves updated static files
  -> Cloudflare CDN delivers to visitors
```

### 6.4 Page Type Architecture

The site has four distinct page types, each with its own Astro approach:

**Blog posts** become Markdown or MDX files in a content collection, rendered via a `BlogPostLayout` that wraps the shared `BaseLayout`.

**Series index pages** are dynamically generated from the content collection grouped by the `series` front matter field, with independent pagination per series.

**Core static pages** (Home, About hub, About me, Follow Me, Contact, Our Work) become individual `.astro` page files under their exact URL paths, all using `BaseLayout`.

**Project pages and deck pages** become individual `.astro` page files under their respective URL paths (`/projects/`, `/deck/`, `/recommendation-engine`), all using `BaseLayout`.

---

## 7. Content Collection Schema

### 7.1 Blog Post Front Matter

```yaml
---
title: "Post Title"
date: 2026-04-01
series: "ai-building-blocks"
seriesLabel: "AI Building Blocks for the Modern Web"
part: 14
description: "One sentence summary for meta description and series card"
ogImage: "/resources/assets/img/blog/2026/ai/topic/hero.png"
tags: ["RAG", "retrieval", "hybrid search"]
canonicalUrl: "https://www.codebrains.co.in/blog/2026/ai/slug"
---
```

The `series` field drives series index pages and pagination grouping. Legacy posts under `/blog/posts/` have no `series` field and appear only on the main blog listing, sorted chronologically with all other posts.

---

## 8. Pagination Requirements

Pagination must be implemented independently on the following pages:

| Page | URL Pattern | Posts Per Page |
|---|---|---|
| Main blog listing | `/blogs` | 10 |
| AI Building Blocks series | `/blog/ai-building-blocks-for-modern-web` | 8 |
| AI Radar series | `/blog/ai-radar` | 8 |
| Any future series | `/blog/[series-slug]` | 8 |

Page 1 is served at the root URL. Subsequent pages follow the pattern `/blogs/2`, `/blogs/3`, `/blog/ai-building-blocks-for-modern-web/2` etc. Astro outputs paginated pages as `.html` files matching the existing site convention.

---

## 9. URL Preservation

All URLs in the inventory in Section 2 must return HTTP 200 with no redirects after migration.

Astro must be configured with `trailingSlash: 'never'` and `build.format: 'file'` so all output uses flat `.html` files that match the current site convention and GitHub Pages serves correctly.

Special attention is required for:
- Legacy posts at `/blog/posts/` which use a different path depth from the AI series posts
- The `/recommendation-engine` project page which sits at the root level, not under `/projects/`
- Deck pages under `/deck/` which are a standalone content type with no collection

---

## 10. Publishing Workflow (Post-Migration)

```
LLM generates blog JSON
  -> Python script converts JSON to .md file with YAML front matter
  -> Script commits .md file and pushes to main
  -> GitHub Actions runs astro build
  -> dist/ pushed to gh-pages branch
  -> GitHub Pages serves updated site
  -> Cloudflare CDN delivers to visitors
  -> Live in approximately 60 to 90 seconds
```

The Python script's responsibility is strictly: produce a correctly structured `.md` file. All layout, SEO tags, series navigation, and pagination is handled by Astro at build time.

---

## 11. Success Metrics

- Zero duplicated header/footer HTML in the repository after migration
- All URLs listed in Section 2 return HTTP 200 with no redirects
- Paginated listing pages work correctly for both series and the main blog listing
- A new blog post can be published by running the Python script and pushing a single `.md` file
- GitHub Actions build completes in under 90 seconds
- No changes required to Cloudflare DNS or CDN configuration

---

## 12. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| URL mismatch on legacy `/blog/posts/` path structure | Medium | Explicit static route for this path in Astro; verify in link checker before cutover |
| `/recommendation-engine` root-level page causes routing conflict | Low | Explicit `src/pages/recommendation-engine.astro` file covers this; verify locally |
| Deck or project pages missed and left as orphaned HTML | Medium | All pages in the Section 2 inventory must be in the pre-cutover verification checklist |
| GitHub Actions build minutes exhausted | Very Low | GitHub provides 2,000 free minutes per month; a 90-second build requires 1,333 pushes per month to approach this limit |
| Astro build breaks on existing image paths | Low | Copy all assets into `public/` at identical relative paths; no content changes needed |

---

## 13. Open Questions

- Should the Python script also auto-commit and push to GitHub, or remain a file generator only?
- Should tags on front matter drive a tag index page (`/tags/rag` etc.) in a future iteration?
- Should a `dev` branch be used for draft posts, with GitHub Actions only deploying from `main`?
- Should the three legacy AEM posts from 2022 be kept under `/blog/posts/` or migrated to the standard `/blog/YYYY/` path structure with redirects?
- Should deck and project pages eventually become their own content collections for easier future management, or remain as individual `.astro` files?
