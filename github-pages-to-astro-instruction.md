# Coding Agent Instructions: Introduce Astro to codebrains.co.in on GitHub Pages

**Project:** codebrains.co.in  
**Reference PRD:** github-pages-to-astro-prd.md

These instructions are written for a coding agent executing this migration end to end. Read the full document before starting any work. Each phase must be completed and verified before moving to the next.

---

## Context

The site is a technical blog currently served as static HTML on GitHub Pages, with Cloudflare as the CDN layer in front. The full page inventory is defined in the PRD Section 2. Every URL in that inventory must resolve identically after migration. The Cloudflare CDN setup and DNS configuration must not be touched. The goal is to introduce Astro as a build layer while keeping GitHub Pages as the host.

The site has four distinct page types that each need a migration approach:

- **Blog posts**: 20 posts across 3 URL patterns (`/blog/2025/ai/`, `/blog/2026/ai/`, `/blog/posts/`)
- **Series index pages**: `/blog/ai-building-blocks-for-modern-web` and `/blog/ai-radar`
- **Core static pages**: Home, About hub, About me, Follow Me, Contact, Our Work, Blogs listing
- **Project and deck pages**: 4 project pages and 3 deck/presentation pages

---

## Phase 1: Scaffold the Astro Project

### 1.1 Initialize Astro Inside the Existing Repository

Do not create a new repository. Run this inside the root of the existing GitHub Pages repo:

```bash
npm create astro@latest . -- --template minimal --no-install
npm install
```

### 1.2 Install Required Dependencies

```bash
npm install @astrojs/mdx
```

### 1.3 Configure astro.config.mjs

The current site uses flat `.html` files (e.g. `blogs.html`, `contactus.html`) rather than per-directory `index.html` files. GitHub Pages serves both patterns, and the existing URLs have no trailing slashes. Astro must be configured to match this convention using `build.format: 'file'`, which outputs `blogs.html` instead of `blogs/index.html`. This keeps all URLs identical to the current site with no behavior change for visitors.

```javascript
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://www.codebrains.co.in',
  integrations: [mdx()],
  output: 'static',
  trailingSlash: 'never',
  build: {
    format: 'file',  // outputs blogs.html not blogs/index.html, matching current site convention
  },
});
```

### 1.4 Update .gitignore

```
dist/
.astro/
node_modules/
```

---

## Phase 2: Create the Shared Layout

### 2.1 Create the Base Layout

Create `src/layouts/BaseLayout.astro`. This is the single file that replaces the duplicated header and footer HTML across every page on the site. Extract the exact header, nav, and footer HTML from the existing site and place them here. Do not alter any CSS classes, IDs, or markup.

```astro
---
const { title, description, ogImage, canonicalUrl } = Astro.props;
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content={description} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={ogImage} />
  <link rel="canonical" href={canonicalUrl} />
  <!-- Copy all existing <link> and <script> tags from the current site <head> here -->
</head>
<body>
  <!-- Copy exact existing header and nav HTML here -->
  <slot />
  <!-- Copy exact existing footer HTML here -->
</body>
</html>
```

### 2.2 Create the Blog Post Layout

Create `src/layouts/BlogPostLayout.astro`:

```astro
---
import BaseLayout from './BaseLayout.astro';
const { frontmatter } = Astro.props;
---
<BaseLayout
  title={frontmatter.title}
  description={frontmatter.description}
  ogImage={frontmatter.ogImage}
  canonicalUrl={frontmatter.canonicalUrl}
>
  <article>
    <h1>{frontmatter.title}</h1>
    <p>{frontmatter.date} | Part {frontmatter.part} of {frontmatter.seriesLabel}</p>
    <slot />
  </article>
</BaseLayout>
```

### 2.3 Copy Static Assets

Copy the entire existing `/resources/` directory into `public/resources/`. Astro serves everything in `public/` at the root path, so all existing image references like `/resources/assets/img/...` resolve identically with no changes to any content.

---

## Phase 3: Define the Content Collection

### 3.1 Create the Collection Config

Create `src/content/config.ts`:

```typescript
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    series: z.string().optional(),
    seriesLabel: z.string().optional(),
    part: z.number().optional(),
    description: z.string(),
    ogImage: z.string(),
    tags: z.array(z.string()).optional(),
    canonicalUrl: z.string(),
  }),
});

export const collections = { blog };
```

### 3.2 Migrate All Blog Posts to Markdown

Create a `.md` file for every blog post listed in the PRD Section 2. The file path under `src/content/blog/` must exactly mirror the URL path of each post.

**AI series posts (2025 and 2026):**

```
src/content/blog/2025/ai/what-is-rag-retrieval-augmented-generation-guide.md
src/content/blog/2025/ai/rag-vs-cag-vs-kag-choosing-right-augmentation-strategy.md
src/content/blog/2025/ai/vector-databases-search-engine-rag-system-actually-needs.md
src/content/blog/2025/ai/model-context-protocol-the-universal-adapter-your-ai-stack-actually-needs.md
src/content/blog/2025/ai/context-rot-silent-performance-killer-in-your-rag-system.md
src/content/blog/2025/ai/context-engineering-the-discipline-your-ai-system-desperately-needs.md
src/content/blog/2025/ai/semantic-cache-smartest-way-to-speed-up-rag.md
src/content/blog/2025/ai/corrective-rag-self-healing-retrieval-layer-your-rag-system-desperately-needs.md
src/content/blog/2026/ai/prompt-caching-the-secret-to-10x-faster-llm-responses.md
src/content/blog/2026/ai/pageIndex-reasoning-based-rag-engine-that-thinks-before-it-retrieves.md
src/content/blog/2026/ai/how-llms-actually-think-transformers-and-attention-explained.md
src/content/blog/2026/ai/when-attention-becomes-bottleneck-how-mamba-is-rethinking-long-context-ai.md
src/content/blog/2026/ai/same-trick-that-made-transformers-great-just-made-them-better.md
src/content/blog/2026/ai/moltbot-the-ai-agent-that-could-be-your-personal-jarvis.md
src/content/blog/2026/ai/moltbook-when-your-ai-gets-a-social-life.md
src/content/blog/2026/ai/when-aem-meets-ai-mcp-turning-content-management-into-conversation.md
src/content/blog/2026/ai/repeat-yourself-how-prompt-repetition-quietly-boosts-llm-accuracy-for-free.md
```

**Legacy AEM posts (2022, no series):**

```
src/content/blog/posts/integratingwookiewithAEM.md
src/content/blog/posts/creatingCustomContentFinderTabAEM.md
src/content/blog/posts/configuringAEMwithMongoMK.md
```

**Front matter for AI series posts:**

```yaml
---
title: "Post Title"
date: 2025-09-30
series: "ai-building-blocks"
seriesLabel: "AI Building Blocks for the Modern Web"
part: 1
description: "One sentence summary"
ogImage: "/resources/assets/img/blog/2025/ai/folder/image.png"
tags: ["tag1", "tag2"]
canonicalUrl: "https://www.codebrains.co.in/blog/2025/ai/slug"
layout: ../../layouts/BlogPostLayout.astro
---
```

**Front matter for legacy posts (no series field):**

```yaml
---
title: "Integrating Apache Wookie with AEM"
date: 2022-10-15
description: "One sentence summary"
ogImage: "/resources/assets/img/mac.jpg"
tags: ["AEM", "Apache Wookie"]
canonicalUrl: "https://www.codebrains.co.in/blog/posts/integratingwookiewithAEM"
layout: ../../../layouts/BlogPostLayout.astro
---
```

Note the deeper relative path in the `layout` field for posts under `/blog/posts/` vs `/blog/YYYY/ai/`.

Extract the body content from each existing HTML file, strip all surrounding layout HTML, and convert the body to Markdown. If a post contains inline SVGs or complex HTML that does not convert cleanly, save it as `.mdx` instead of `.md`.

---

## Phase 4: Dynamic Routing for Blog Posts

### 4.1 Create the Post Route

Create `src/pages/blog/[...slug].astro`. This single file handles all blog posts regardless of URL depth, including both the `/blog/2025/ai/` and `/blog/posts/` path structures.

```astro
---
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---
<Content />
```

Because each post declares a `layout` in its front matter, Astro wraps the rendered content in `BlogPostLayout` automatically. No additional logic is needed here.

---

## Phase 5: Pagination

### 5.1 Paginated Main Blog Listing

Create `src/pages/blogs/[...page].astro`. This generates the main `/blogs` page with all posts sorted by date, including legacy posts. Page 1 renders at `/blogs`, page 2 at `/blogs/2` etc.

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';

export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  const sorted = posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
  return paginate(sorted, { pageSize: 10 });
}

const { page } = Astro.props;
---
<BaseLayout title="Blogs | codebrains.co.in" description="All blog posts">
  {page.data.map(post => (
    <article>
      <img src={post.data.ogImage} alt={post.data.title} loading="lazy" />
      <h3><a href={`/blog/${post.slug}`}>{post.data.title}</a></h3>
      <p>{post.data.date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
      <p>{post.data.description}</p>
      <a href={`/blog/${post.slug}/`}>Read more</a>
    </article>
  ))}
  <nav>
    {page.url.prev && <a href={page.url.prev}>Previous</a>}
    {page.url.next && <a href={page.url.next}>Next</a>}
  </nav>
</BaseLayout>
```

### 5.2 Paginated Series Index Pages

Create `src/pages/blog/[series]/[...page].astro`. This single file generates paginated index pages for every series automatically. Adding a new series in future requires no routing changes.

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';

export async function getStaticPaths({ paginate }) {
  const allPosts = await getCollection('blog');

  const seriesSlugs = [...new Set(
    allPosts
      .filter(p => p.data.series)
      .map(p => p.data.series)
  )];

  return seriesSlugs.flatMap(series => {
    const seriesPosts = allPosts
      .filter(p => p.data.series === series)
      .sort((a, b) => (a.data.part ?? 0) - (b.data.part ?? 0));

    return paginate(seriesPosts, {
      params: { series },
      pageSize: 8,
    });
  });
}

const { page, params } = Astro.props;
const seriesLabel = page.data[0]?.data.seriesLabel ?? params.series;
---
<BaseLayout title={`${seriesLabel} | codebrains.co.in`} description={seriesLabel}>
  <h1>{seriesLabel}</h1>
  {page.data.map(post => (
    <article>
      <img src={post.data.ogImage} alt={post.data.title} loading="lazy" />
      <span>Part {post.data.part}</span>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      <p>{post.data.description}</p>
    </article>
  ))}
  <nav>
    {page.url.prev && <a href={page.url.prev}>Previous</a>}
    {page.url.next && <a href={page.url.next}>Next</a>}
  </nav>
</BaseLayout>
```

---

## Phase 6: Migrate All Static Pages

Each of these pages must be created as an individual `.astro` file. For each one: copy the existing page body HTML from the current live site and paste it as the `<slot />` content inside `BaseLayout`. Do not rewrite or redesign the content.

### 6.1 Core Site Pages

| File to create | Source URL to copy from |
|---|---|
| `src/pages/index.astro` | `https://www.codebrains.co.in/` |
| `src/pages/ankitgubrani.astro` | `https://www.codebrains.co.in/ankitgubrani` |
| `src/pages/about/ankitgubrani.astro` | `https://www.codebrains.co.in/about/ankitgubrani` |
| `src/pages/followme.astro` | `https://www.codebrains.co.in/followme` |
| `src/pages/contactus.astro` | `https://www.codebrains.co.in/contactus` |
| `src/pages/projects.astro` | `https://www.codebrains.co.in/projects` |

Each file follows this structure:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout
  title="Page Title | codebrains.co.in"
  description="Page description"
  ogImage="/resources/assets/img/..."
  canonicalUrl="https://www.codebrains.co.in/page-path"
>
  <!-- Paste the body content of the existing page here exactly -->
</BaseLayout>
```

### 6.2 Project Pages

| File to create | Source URL to copy from |
|---|---|
| `src/pages/recommendation-engine.astro` | `https://www.codebrains.co.in/recommendation-engine` |
| `src/pages/projects/offline-webpage-editor.astro` | `https://www.codebrains.co.in/projects/offline-webpage-editor` |
| `src/pages/projects/aem-mahout-connector.astro` | `https://www.codebrains.co.in/projects/aem-mahout-connector` |
| `src/pages/projects/aem-wookie-connector.astro` | `https://www.codebrains.co.in/projects/aem-wookie-connector` |

Note that `recommendation-engine.astro` sits directly under `src/pages/`, not under `src/pages/projects/`, because the existing URL is `/recommendation-engine` not `/projects/recommendation-engine`.

### 6.3 Deck / Presentation Pages

| File to create | Source URL to copy from |
|---|---|
| `src/pages/deck/sling-pipes.astro` | `https://www.codebrains.co.in/deck/sling-pipes` |
| `src/pages/deck/circuit-breaker-pattern.astro` | `https://www.codebrains.co.in/deck/circuit-breaker-pattern` |
| `src/pages/deck/unit-testing-and-mocking.astro` | `https://www.codebrains.co.in/deck/unit-testing-and-mocking` |

---

## Phase 7: GitHub Actions Deployment Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build Astro site
        run: npm run build

      - name: Upload pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

After adding this file, go to the repository Settings > Pages and change the source from "Deploy from a branch" to **"GitHub Actions"**. This is required for the official `actions/deploy-pages` action to work. You do not need to configure the `gh-pages` branch at all with this approach; GitHub manages the deployment target internally.

---

## Phase 8: Update the Python Publishing Script

The Python script currently generates a full HTML file. After this migration it must generate a `.md` file with correct YAML front matter placed in the right directory.

### 8.1 New Script Output Contract

Input JSON shape:

```json
{
  "title": "Post Title",
  "date": "2026-04-01",
  "series": "ai-building-blocks",
  "seriesLabel": "AI Building Blocks for the Modern Web",
  "part": 14,
  "description": "One sentence summary",
  "ogImage": "/resources/assets/img/blog/2026/ai/topic/hero.png",
  "tags": ["tag1", "tag2"],
  "slug": "post-slug",
  "year": "2026",
  "body": "Full blog post content in Markdown"
}
```

Output file location: `src/content/blog/{year}/ai/{slug}.md`

Output file content:

```
---
title: "{title}"
date: {date}
series: "{series}"
seriesLabel: "{seriesLabel}"
part: {part}
description: "{description}"
ogImage: "{ogImage}"
tags: {tags}
canonicalUrl: "https://www.codebrains.co.in/blog/{year}/ai/{slug}"
layout: ../../../../layouts/BlogPostLayout.astro
---

{body}
```

### 8.2 Optional: Auto-Push Step

Add an optional `--push` flag:

```bash
git add src/content/blog/{year}/ai/{slug}.md
git commit -m "publish: {title}"
git push origin main
```

GitHub Actions detects the push to `main`, builds, and deploys. The post is live in approximately 60 to 90 seconds.

---

## Phase 9: Pre-Cutover Verification

Run the full build locally before merging anything to `main`:

```bash
npm run build
npm run preview
```

Run a link checker against `http://localhost:4321`. Every URL in the PRD Section 2 inventory must return HTTP 200 before proceeding.

### Verification Checklist

**Blog posts (all 20):**
- [ ] All 17 AI series posts under `/blog/2025/ai/` and `/blog/2026/ai/` return 200
- [ ] All 3 legacy posts under `/blog/posts/` return 200

**Listing and series pages:**
- [ ] `/blogs/` loads with 10 posts and pagination controls
- [ ] `/blogs/2/` loads correctly
- [ ] `/blog/ai-building-blocks-for-modern-web/` loads with posts in part order
- [ ] `/blog/ai-radar/` loads correctly
- [ ] Series pages paginate at 8 posts when count exceeds 8

**Core static pages:**
- [ ] `/` (Home) renders correctly
- [ ] `/ankitgubrani/` renders correctly
- [ ] `/about/ankitgubrani/` renders correctly
- [ ] `/followme/` renders correctly
- [ ] `/contactus/` renders correctly
- [ ] `/projects/` renders correctly

**Project pages:**
- [ ] `/recommendation-engine/` renders correctly
- [ ] `/projects/offline-webpage-editor/` renders correctly
- [ ] `/projects/aem-mahout-connector/` renders correctly
- [ ] `/projects/aem-wookie-connector/` renders correctly

**Deck pages:**
- [ ] `/deck/sling-pipes/` renders correctly
- [ ] `/deck/circuit-breaker-pattern/` renders correctly
- [ ] `/deck/unit-testing-and-mocking/` renders correctly

**Quality checks:**
- [ ] Open Graph tags present and correct on all blog post pages
- [ ] Header and footer render identically to the current live site on all page types
- [ ] All images load with no broken paths
- [ ] Python script generates a valid `.md` file for a test post and `astro build` succeeds with it

After merging to `main`, verify GitHub Actions completes successfully and the live site at codebrains.co.in reflects the changes. Cloudflare does not need any reconfiguration.

---

## Final File Structure Reference

```
codebrains.co.in/
  .github/
    workflows/
      deploy.yml
  public/
    resources/              # all existing site assets at identical paths
  src/
    content/
      config.ts
      blog/
        2025/
          ai/               # 8 AI Building Blocks posts
        2026/
          ai/               # 9 AI series posts (Building Blocks + AI Radar)
        posts/              # 3 legacy AEM posts from 2022
    layouts/
      BaseLayout.astro
      BlogPostLayout.astro
    pages/
      index.astro                         # /
      ankitgubrani.astro                  # /ankitgubrani
      followme.astro                      # /followme
      contactus.astro                     # /contactus
      projects.astro                      # /projects
      recommendation-engine.astro         # /recommendation-engine
      about/
        ankitgubrani.astro                # /about/ankitgubrani
      blogs/
        [...page].astro                   # /blogs, /blogs/2, etc.
      blog/
        [...slug].astro                   # all blog post routes
        [series]/
          [...page].astro                 # series index pages with pagination
      projects/
        offline-webpage-editor.astro
        aem-mahout-connector.astro
        aem-wookie-connector.astro
      deck/
        sling-pipes.astro
        circuit-breaker-pattern.astro
        unit-testing-and-mocking.astro
  astro.config.mjs
  package.json
```

---

## Notes for the Agent

- Do not touch any Cloudflare settings, DNS records, or the existing Cloudflare proxy configuration.
- Preserve all existing CSS classes and HTML structure inside every layout and page file. Do not restyle anything.
- When converting HTML post bodies to Markdown, preserve inline SVGs by pasting them directly. Astro renders raw HTML inside `.md` files.
- The `layout` field in front matter must use a relative path from the `.md` file to the layout file. The depth of this path changes between `/blog/2025/ai/` posts (4 levels deep: `../../../../layouts/BlogPostLayout.astro`) and `/blog/posts/` posts (3 levels deep: `../../../layouts/BlogPostLayout.astro`).
- All internal `href` values should not use trailing slashes, matching the `trailingSlash: 'never'` config.
- If a post body does not convert cleanly to Markdown, use `.mdx` instead of `.md`.
- The GitHub Actions workflow uses the official `actions/deploy-pages` action. For this to work, go to repository Settings > Pages and set the source to "GitHub Actions" rather than "Deploy from a branch" before the first run.
- When copying deck pages, check whether they embed external iframes or scripts (e.g. SlideShare, Google Slides). If they do, the iframe embed can be pasted directly into the `.astro` file body and will render correctly.
