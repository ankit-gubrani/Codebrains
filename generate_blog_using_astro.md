# How to Generate a New Blog Post (Astro MDX)

This guide explains how to publish a new blog post on **codebrains.co.in** using the Astro-based workflow. All posts now use the **.mdx** format for consistent support of inline HTML, SVGs, and interactive components.

---

## Prerequisites

- **Node.js ≥ 22.12.0** installed
- **Python 3** installed (with `markdownify` package — auto-installed on first run)
- Repository cloned locally

---

## Step-by-Step

### 1. Prepare your `blog.json`

Edit the `blog.json` file in the project root with the new post's data.

```json
{
  "title": "Your Blog Title Here",
  "category": "ai",
  "keywords": "keyword1, keyword2, keyword3",
  "description": "A short SEO-friendly meta description",
  "intro": "A 1–2 sentence intro shown on index cards",
  "imagePath": "resources/assets/img/blog/2026/ai/your-folder/hero.png",
  "html": "<article class=\"blog-post\">...your HTML content...</article>"
}
```

### 2. Run the publishing script

```bash
python3 generate_blog.py
```

This will:
- Convert the HTML content to **Markdown**
- Escape characters that clash with JSX (like `{` and `}`) inside your post content
- Convert HTML comments to MDX comments `{/* ... */}`
- Generate YAML **frontmatter**
- Write the **.mdx** file to `src/content/blog/<year>/<category>/<slug>.mdx`

### 3. (Optional) Add series metadata

If the post belongs to a series, manually add these fields to the generated `.mdx` frontmatter:

```yaml
series: "ai-building-blocks"
seriesLabel: "AI Building Blocks for the Modern Web"
part: 14
```

### 4. Build and preview

```bash
npm run build    # Compile all pages
npm run preview  # Preview at http://localhost:4321
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| Unexpected character `{` or `}` | MDX treats curly braces as JS. Use `&#123;` and `&#125;` instead. `generate_blog.py` handles this automatically. |
| HTML comments cause build errors | Use MDX comments: `{/* your comment */}`. `generate_blog.py` handles this automatically. |
| Blog page has no styles/header | Ensure the `.mdx` file has `layout: ../../../layouts/BlogPostLayout.astro` in its frontmatter. |