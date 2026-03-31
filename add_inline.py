import os
import re

def fix_inline(content):
    def replacer(match):
        tag = match.group(0)
        if "is:inline" in tag or "ld+json" in tag:
            return tag
        return tag.replace("<script", "<script is:inline")

    new_content = re.sub(r'<script\b[^>]*>', replacer, content)
    return new_content

for root, _, files in os.walk("src/pages"):
    for f in files:
        if f.endswith(".astro"):
            path = os.path.join(root, f)
            with open(path, "r", encoding='utf-8') as file:
                content = file.read()
            
            new_content = fix_inline(content)
            if new_content != content:
                with open(path, "w", encoding='utf-8') as file:
                    file.write(new_content)
                print(f"Added is:inline to scripts in {path}")
