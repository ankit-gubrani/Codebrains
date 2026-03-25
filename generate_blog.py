import json
import re
import os
import sys
from datetime import datetime

# Schema for blog.json:
# {
#   "title": "Blog Title",
#   "category": "ai",
#   "keywords": "AI, Tech, Blog",
#   "description": "Blog description",
#   "intro": "Blog intro text",
#   "imagePath": "resources/assets/img/blog/2026/ai/image.png",
#   "html": "<article class=\"blog-post\">...</article>"
# }

def generate_slug(title):
    # Lowercase and replace non-alphanumeric (except spaces/dashes) with empty
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
    # Replace spaces with dashes
    slug = re.sub(r'\s+', '-', slug)
    return slug

def main():
    if not os.path.exists('blog.json'):
        print("Error: blog.json not found in the current directory.")
        sys.exit(1)

    with open('blog.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Required fields
    required = ['title', 'category', 'keywords', 'description', 'intro', 'imagePath', 'html']
    for req in required:
        if req not in data:
            print(f"Error: missing required field '{req}' in blog.json")
            sys.exit(1)

    title = data['title']
    slug = generate_slug(title)
    
    # Handle dates
    now = datetime.now()
    year_str = str(now.year)
    date_iso = now.strftime('%Y-%m-%d')
    date_readable = now.strftime('%B %-d, %Y')  # e.g., March 25, 2026

    # 1. Create the blog HTML file from template
    with open('blog-template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    template = template.replace('{{TITLE}}', title)
    template = template.replace('{{DESCRIPTION}}', data['description'])
    template = template.replace('{{KEYWORDS}}', data['keywords'])
    template = template.replace('{{IMAGE_PATH}}', data['imagePath'])
    template = template.replace('{{DATE_ISO}}', date_iso)
    template = template.replace('{{DATE_READABLE}}', date_readable)
    template = template.replace('{{YEAR}}', year_str)
    template = template.replace('{{CATEGORY}}', data['category'])
    template = template.replace('{{CATEGORY_LABEL}}', data['category'].upper())
    template = template.replace('{{SLUG}}', slug)
    template = template.replace('{{BLOG_HTML}}', data['html'])

    # Ensure output directory exists
    out_dir = os.path.join('blog', year_str, data['category'])
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"{slug}.html")

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Created blog post file: {out_file}")

    # 2. Update blogs.html
    blogs_html_path = 'blogs.html'
    if os.path.exists(blogs_html_path):
        with open(blogs_html_path, 'r', encoding='utf-8') as f:
            blogs_content = f.read()

        # Find the first blog-card-wrapper and insert before it
        search_str = '<div class="blog-card-wrapper">'
        insert_idx = blogs_content.find(search_str)
        if insert_idx != -1:
            # find the indentation before the wrapper
            line_start = blogs_content.rfind('\n', 0, insert_idx) + 1
            indent = blogs_content[line_start:insert_idx]
            
            blog_card = f"""<div class="blog-card-wrapper">
{indent}    <div class="blog-card">
{indent}        <div class="card-image">
{indent}            <img src="./{data['imagePath']}" alt="{title}">
{indent}        </div>
{indent}        <h3><a href="https://www.codebrains.co.in/blog/{year_str}/{data['category']}/{slug}">{title}</a></h3>
{indent}        <div class="date">{date_readable}</div>
{indent}        <div class="description">
{indent}            <p>{data['intro']}</p>
{indent}        </div>
{indent}        <a href="https://www.codebrains.co.in/blog/{year_str}/{data['category']}/{slug}" class="read-more">Read more</a>
{indent}    </div>
{indent}</div>
{indent}"""
            blogs_content = blogs_content[:insert_idx] + blog_card + blogs_content[insert_idx:]
            with open(blogs_html_path, 'w', encoding='utf-8') as f:
                f.write(blogs_content)
            print("Updated blogs.html")
        else:
            print("Warning: Could not find <div class=\"blog-card-wrapper\"> in blogs.html")

    # 3. Update index.html
    index_html_path = 'index.html'
    if os.path.exists(index_html_path):
        with open(index_html_path, 'r', encoding='utf-8') as f:
            index_content = f.read()

        content_a_idx = index_content.find('<div class="content-section-a">')
        content_b_idx = index_content.find('<div class="content-section-b">')

        # Determine the class of the very first section
        # We only consider the ones that appear after the header to prepend to the top of the list
        search_start = index_content.find('<div class="content-section-')
        
        is_next_a = True
        if content_a_idx != -1 and content_b_idx != -1:
            if content_b_idx < content_a_idx:
                is_next_a = False
        elif content_b_idx != -1:
            is_next_a = False

        hero_url = f"https://www.codebrains.co.in/blog/{year_str}/{data['category']}/{slug}"

        if is_next_a:
            # Current top is A, new one should be B
            index_card = f"""<div class="content-section-b">
    <div class="container">
        <div class="row">
            <div class="col-lg-5 col-sm-6">
                <h2 class="section-heading">
                    <a href="{hero_url}" target="_blank">{title}</a>
                </h2>
                <p class="lead">{data['intro']}
                    <a href="{hero_url}" target="_blank"> Continue Reading...</a></p>
                </p>
            </div>
            <div class="col-lg-5 col-lg-offset-2 col-sm-6">
                <a href="{hero_url}" target="_blank">
                    <img class="img-responsive curvedImage" src="./{data['imagePath']}" alt="{title}">
                </a>
            </div>
        </div>
    </div>
</div>
"""
        else:
            # Current top is B, new one should be A
            index_card = f"""<div class="content-section-a">
    <div class="container">
        <div class="row">
            <div class="col-lg-5 col-lg-offset-1 col-sm-push-6 col-sm-6">
                <h2 class="section-heading">
                    <a href="{hero_url}" target="_blank">{title}</a>
                </h2>
                <p class="lead">{data['intro']}   
                    <a href="{hero_url}" target="_blank"> Continue Reading...</a></p>
            </div>
            <div class="col-lg-5 col-sm-pull-6  col-sm-6">
                <a href="{hero_url}" target="_blank">
                    <img class="img-responsive curvedImage" src="./{data['imagePath']}" alt="{title}"> 
                </a>
            </div>
        </div>
    </div>
</div>
"""
        
        if search_start != -1:
            index_content = index_content[:search_start] + index_card + index_content[search_start:]
            with open(index_html_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print("Updated index.html")
        else:
            print("Warning: Could not find <div class=\"content-section-\"> in index.html")

    print("Success! The new blog post has been generated and integrated.")

if __name__ == '__main__':
    main()
