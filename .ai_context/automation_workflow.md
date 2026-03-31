# Blog Automation & Content Workflow

This directory contains Python automation scripts for converting raw JSON input into MDX files that Astro can consume.

## The Posting Workflow

To create a new blog post, the author strictly follows this process:
1. Open `blog.json`.
2. Populate the required keys: `title`, `description`, `intro`, `category`, `series`, `seriesLabel`, `keywords` (comma-separated), `heroImage` (optional path to a display image), and the `html` content block.
3. Run the generator script:
   ```bash
   python3 generate_blog.py
   ```
4. The script creates an MDX file in the correct chronological path (e.g., `src/content/blog/2026/ai/my-blog-post-slug.mdx`).

## `generate_blog.py` Mechanics
The script automatically handles several specific processing rules:
- **Slugification**: Converts the `title` into a URL-safe `slug`.
- **Frontmatter Injection**: Appends exactly identical keys expected by the Zod schema in `src/content.config.ts`.
- **Date Handling**: Defaults to the current date, but reads a `<time>` tag within the HTML author block if present.
- **MDX SVG Compatibility**: The script intercepts any `<svg>` elements inside the HTML block and modifies their inner text contents. It forces multi-line `<text>` elements onto a single line to prevent Astro's MDX parser from injecting stray `<p>` tags into SVG coordinates.

## Legacy Posts
Legacy HTML posts from the pre-Astro static era were processed using `migrate_legacy.py`, migrating them dynamically into MDX. This script is generally inactive for day-to-day use but contains the logic for handling legacy CSS layouts inside MDX.
