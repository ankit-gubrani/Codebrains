Blog Generation Automation Walkthrough

blog-template.html
: A generic HTML template based on your previous blogs. It includes placeholders for all dynamic metadata.
generate_blog.py
: A robust python script that:
Reads 
blog.json
.
Populates the template.
Saves it to the correct blog/YYYY/category/slug.html folder.
Automatically injects the new blog card into the top of 
blogs.html
.
Automatically injects the new blog card into the top of 
index.html
 (smartly alternating between the content-section-a and content-section-b classes so the layout never breaks!).
Step-by-Step Guide
Here is how you use the new automation process:

Step 1: Tell your LLM to generate 
blog.json
You can provide your LLM with the following prompt:

```text
Please write my new blog post.

**Instructions for the blog:**
- Match the tone, clarity, and structure of this blog: https://www.codebrains.co.in/blog/2026/ai/how-llms-actually-think-transformers-and-attention-explained
- Write in a simple, clear, and conversational tone
- Avoid jargon unless explained
- Mention about the latest paper release about new Block attention residual https://arxiv.org/abs/2603.15031 and include a link to paper
- Do NOT use em dashes
- Use real-world analogies where helpful
- Keep paragraphs short and readable
- Make it engaging for engineers and architects
- Generate the SVGs for the blog to explain concepts in the blog
- Make all the important sections of the blog in <strong> tag

Add the Blog in this Div structure:
<article class="blog-post">
            <header>
                <h1>BLOG HEADING</h1>
                <p class="blog-author-info">
                    By <span>Ankit Gubrani</span> on
                    <time datetime="2026-01-28">January 28, 2026</time>
                </p>
                <label class="eyebrow-blue"><strong>AI Radar: Tracking AI Innovations</strong></label>
            </header>
            <div class="blog-content"> <section class="what-is-claudebot">
                    <h2><strong>FIRST SUB HEADING</strong></h2>
                    ADD BLOG CONTENT
            </div>
</article>

Output a single JSON object in this exact schema saved as `blog.json`:
{
  "title": "Your Blog Title",
  "category": "ai", // or your desired category
  "keywords": "Comma, Separated, Keywords",
  "description": "A short meta description for SEO.",
  "intro": "A short 1-2 sentence intro used for the homepage cards.",
  "imagePath": "resources/assets/img/blog/2026/ai/image.png",
  "html": "<article class=\"blog-post\">... the generated HTML content matching the div structure above ...</article>"
}
```
Step 2: Generate the image
Generate your image using an LLM/generator exactly as you do now, and place it in the path you defined in imagePath within 
blog.json
 (e.g. resources/assets/img/blog/2026/ai/my-new-blog/hero.png).

Step 3: Run the Script
From the root of your Codebrains repository, simply run:

bash
python3 generate_blog.py
Step 4: Review and Commit!
That's it! The script will create your new HTML page under blog/2026/... and correctly wire it up in 
index.html
 and 
blogs.html
. Run git diff to see the magic, and then git commit.