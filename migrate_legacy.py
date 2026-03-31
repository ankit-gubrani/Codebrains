import os
import re
from bs4 import BeautifulSoup
from markdownify import markdownify as md

blog_dirs = ["blog/posts"]
output_base = "src/content/blog"

allowed_tags = {'img', 'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'ellipse', 'text', 'tspan', 'defs', 'linearGradient', 'stop', 'marker', 'g', 'br', 'hr', 'code', 'section', 'article', 'header', 'footer', 'div', 'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'pre', 'a', 'time', 'label', 'strong', 'em', 'del', 'sup', 'sub', 'details', 'summary', 'canvas', 'figure', 'figcaption'}

def mdx_escape_tag(match):
    tag_content = match.group(1)
    tag_name = re.split(r'[\s/>]', tag_content)[0].lower()
    if tag_name in allowed_tags:
        return match.group(0)
    else:
        return f"&lt;{tag_content}&gt;"

for d in blog_dirs:
    if not os.path.exists(d): continue
    for f in os.listdir(d):
        if f.endswith('.html'):
            filepath = os.path.join(d, f)
            with open(filepath, 'r', encoding='utf-8') as html_file:
                soup = BeautifulSoup(html_file.read(), 'html.parser')
            
            title = soup.title.string.strip() if soup.title else f
            
            desc_meta = soup.find('meta', attrs={'name': 'Description'})
            desc = desc_meta['content'] if desc_meta else "Legacy AEM post"
            
            og_img = soup.find('meta', property='og:image')
            og_img = og_img['content'] if og_img else ""
            if og_img.startswith('https://www.codebrains.co.in'):
                og_img = og_img.replace('https://www.codebrains.co.in', '')
            
            tags_meta = soup.find('meta', attrs={'name': 'Keywords'})
            tags = [t.strip() for t in tags_meta['content'].split(',')] if tags_meta else ["AEM"]
            
            date = "2022-10-15"
            canonical = f"https://www.codebrains.co.in/{d}/{f.replace('.html', '')}"

            content_div = soup.find('div', class_='main-container')
            if not content_div: continue

            markdown_body = md(str(content_div), heading_style="ATX")
            markdown_body = markdown_body.replace("../../resources/assets/img/", "../../../assets/img/")

            # MDX Safety Fixes
            # 1. Escape angle brackets that aren't allowed tags
            markdown_body = re.sub(r'<([^>]+)>', mdx_escape_tag, markdown_body)
            # 2. Escape standalone < signs
            markdown_body = re.sub(r'<(?!([a-zA-Z/!?]))', '&lt;', markdown_body)
            # 3. Escape { and }
            markdown_body = markdown_body.replace('{', '&#123;').replace('}', '&#125;')
            # 4. Escape 'export' or 'import' at the start of a line (MDX treats them as JS)
            markdown_body = re.sub(r'^(export|import)\s', r'\\\1 ', markdown_body, flags=re.MULTILINE)

            frontmatter = []
            frontmatter.append("---")
            frontmatter.append(f'title: "{title.replace(chr(34), chr(39))}"')
            frontmatter.append(f"date: {date}")
            frontmatter.append(f'description: "{desc.replace(chr(34), chr(39))}"')
            frontmatter.append(f'ogImage: "{og_img}"')
            if og_img:
                frontmatter.append(f'heroImage: "{og_img}"')
            tags_str = ", ".join([f'"{t}"' for t in tags])
            frontmatter.append(f'tags: [{tags_str}]')
            frontmatter.append(f'canonicalUrl: "{canonical}"')
            frontmatter.append("---")
            frontmatter.append("")
            frontmatter.append(markdown_body.strip())
            
            out_dir = os.path.join(output_base, d.replace("blog/", ""))
            os.makedirs(out_dir, exist_ok=True)
            out_filepath = os.path.join(out_dir, f.replace('.html', '.mdx'))
            with open(out_filepath, 'w', encoding='utf-8') as out_file:
                out_file.write("\n".join(frontmatter))
            print(f"Migrated legacy: {filepath} -> {out_filepath}")
