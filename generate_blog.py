import json
import re
import os
import sys
from datetime import datetime

try:
    from markdownify import markdownify as md
except ImportError:
    print("Warning: markdownify not found. Installing now...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdownify", "--user"])
    from markdownify import markdownify as md

def generate_slug(title):
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    slug = re.sub(r'\s+', '-', slug)
    return slug

def main():
    if not os.path.exists('blog.json'):
        print("Error: blog.json not found in the current directory.")
        sys.exit(1)

    with open('blog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    required = ['title', 'category', 'keywords', 'description', 'intro', 'imagePath', 'html']
    for req in required:
        if req not in data:
            print(f"Error: missing required field '{req}' in blog.json")
            sys.exit(1)

    title = data['title']
    slug = generate_slug(title)
    
    now = datetime.now()
    year_str = str(now.year)
    date_iso = now.strftime('%Y-%m-%d')

    # Convert image path to root relative for standard Astro resolving
    image_path = data['imagePath']
    if not image_path.startswith('/'):
        image_path = '/' + image_path

    # Extract series and hero info
    series = data.get('series', '')
    series_label = data.get('seriesLabel', '')
    hero_image = data.get('heroImage', '')

    # Convert HTML to Markdown
    html_content = data['html']
    
    # Strip <header>...</header> if it exists to avoid duplication with BlogPostLayout.astro
    html_content = re.sub(r'<header>.*?</header>', '', html_content, flags=re.DOTALL)
    
    # Protect SVGs with placeholders before markdownify
    svg_placeholders = []
    def save_svg(match):
        svg_placeholders.append(match.group(0))
        return f'ASVGDOCUMENT{len(svg_placeholders)-1}END'
    
    html_content = re.sub(r'<svg.*?</svg>', save_svg, html_content, flags=re.DOTALL)

    markdown_content = md(html_content, heading_style="ATX", default_title=True)
    
    # Identify "fake" tags (like <CONTEXT>) that are not valid HTML/SVG and escape them
    # MDX-JS treats any <[a-zA-Z] as a JSX component start.
    allowed_tags = {'img', 'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'text', 'tspan', 'defs', 'linearGradient', 'stop', 'marker', 'g', 'br', 'hr', 'code', 'section', 'article', 'header', 'footer', 'div', 'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'pre', 'a', 'time', 'label', 'strong', 'em', 'del', 'sup', 'sub', 'details', 'summary', 'canvas', 'figure', 'figcaption'}
    
    def mdx_escape(match):
        tag_content = match.group(1)
        tag_name = re.split(r'[\s/>]', tag_content)[0].lower()
        if tag_name in allowed_tags or tag_name.startswith('asvgdocument'):
            return match.group(0) # Keep as is (placeholders are safe)
        else:
            return f"&lt;{tag_content}&gt;" # Escape
            
    # Find anything that looks like a tag: <something>
    markdown_content = re.sub(r'<([^>]+)>', mdx_escape, markdown_content)

    # Restore SVGs
    for i, svg in enumerate(svg_placeholders):
        # Escape characters that break MDX inside SVG text
        # We need to preserve the SVG tags themselves though.
        # Strategy: Escape < if it's not followed by a known SVG tag name or /
        svg_tags = {'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'text', 'tspan', 'defs', 'linearGradient', 'stop', 'marker', 'g', 'use', 'image'}
        
        # 1. Convert HTML comments to MDX comments
        svg = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', svg)
        
        # 2. Escape angle brackets that aren't part of a valid tag
        # This is tricky with regex, so let's just target the known problematic ones in this specific blog
        # and also a general rule for < followed by space or anything not a tag name.
        svg = svg.replace('<CONTEXT>', '&lt;CONTEXT&gt;')
        svg = svg.replace('<QUESTION>', '&lt;QUESTION&gt;')
        svg = svg.replace('<QUERY>', '&lt;QUERY&gt;')
        
        markdown_content = markdown_content.replace(f'ASVGDOCUMENT{i}END', svg)

    # Wrap images in <figure> tag as requested
    # Supports both Markdown ![]() and HTML <img>
    def wrap_image(match):
        img_tag = match.group(0)
        return f'<figure style="text-align: center;" class="blog-image-square-wrap">\n{img_tag}\n</figure>'
    
    # Wrap Markdown images
    markdown_content = re.sub(r'(!\[.*?\]\(.*?\))', wrap_image, markdown_content)
    # Wrap HTML img tags (if any)
    markdown_content = re.sub(r'(<img.*?>)', wrap_image, markdown_content)

    # Replace HTML comments with MDX comments
    markdown_content = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', markdown_content, flags=re.DOTALL)
    
    # Save MDX comments so we don't escape their braces
    comments = []
    def save_comment(m):
        comments.append(m.group(0))
        return f'MDXCOMMENT{len(comments)-1}END'
    markdown_content = re.sub(r'\{/\*.*?\*/\}', save_comment, markdown_content, flags=re.DOTALL)
    
    # Escape remaining curly braces (SVG style attributes etc)
    markdown_content = markdown_content.replace('{', '&#123;').replace('}', '&#125;')
    
    # Escape < signs that are not part of an HTML tag
    markdown_content = re.sub(r'<(?!([a-zA-Z/!?]))', '&lt;', markdown_content)
    
    # Restore MDX comments
    for i, c in enumerate(comments):
        markdown_content = markdown_content.replace(f'MDXCOMMENT{i}END', c)
    
    # Process keywords to array
    tags = [t.strip() for t in data['keywords'].split(',') if t.strip()]
    tags_str = ", ".join([f'"{t}"' for t in tags])

    layout_depth = "../../../../layouts/BlogPostLayout.astro"

    post_url_path = f"{year_str}/{data['category']}/{slug}"
    canonical = f"https://www.codebrains.co.in/blog/{post_url_path}"

    frontmatter = []
    frontmatter.append("---")

    frontmatter.append(f'title: "{title.replace(chr(34), chr(39))}"')
    frontmatter.append(f"date: {date_iso}")
    if series:
        frontmatter.append(f'series: "{series}"')
    if series_label:
        frontmatter.append(f'seriesLabel: "{series_label}"')
    if hero_image:
        frontmatter.append(f'heroImage: "{hero_image}"')
    frontmatter.append(f'description: "{data["description"].replace(chr(34), chr(39))}"')
    frontmatter.append(f'ogImage: "{image_path}"')
    if tags:
        frontmatter.append(f'tags: [{tags_str}]')
    frontmatter.append(f'canonicalUrl: "{canonical}"')
    frontmatter.append("---")
    frontmatter.append("")
    frontmatter.append(markdown_content.strip())
    
    out_dir = os.path.join('src/content/blog', year_str, data['category'])
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{slug}.mdx")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(frontmatter))
    print(f"Created Astro blog post: {out_file}")
    print("Run `npm run build` to automatically update the sitemap and all index pages!")

if __name__ == '__main__':
    main()
