import os
import re

def escape_astro_braces(html):
    parts = re.split(r'(?i)(<script.*?</script>|<style.*?</style>)', html, flags=re.DOTALL)
    for i in range(len(parts)):
        if i % 2 == 0:
            parts[i] = parts[i].replace('{', '&#123;').replace('}', '&#125;')
    return "".join(parts)

def fix_dir(d):
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.astro'):
                path = os.path.join(root, f)
                with open(path, 'r') as file:
                    content = file.read()
                
                # We need to escape only the content inside BaseLayout, or just the whole file?
                # The whole file might have `canonicalUrl={<something>}` which contains `{`.
                # Let's split by <BaseLayout and </BaseLayout>
                parts = content.split('<BaseLayout')
                if len(parts) > 1:
                    header = parts[0]
                    rest = '<BaseLayout' + parts[1]
                    # The props might contain { } so let's find the closing >
                    layout_tag_end = rest.find('>')
                    if layout_tag_end != -1:
                        layout_tag = rest[:layout_tag_end+1]
                        inner = rest[layout_tag_end+1:]
                        inner_parts = inner.rsplit('</BaseLayout>', 1)
                        if len(inner_parts) == 2:
                            inner_html = inner_parts[0]
                            footer = '</BaseLayout>' + inner_parts[1]
                            escaped_inner = escape_astro_braces(inner_html)
                            new_content = header + layout_tag + escaped_inner + footer
                            with open(path, 'w') as out:
                                out.write(new_content)
                                print(f"Fixed {path}")

fix_dir('src/pages/deck')
fix_dir('src/pages/projects')
fix_dir('src/pages/about')
# also index, contactus, ankitgubrani, recommendation-engine
fix_dir('src/pages')

