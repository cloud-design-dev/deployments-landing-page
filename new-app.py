from flask import Flask, render_template
from markdown2 import Markdown
import os
import frontmatter

app = Flask(__name__)

@app.route('/')
def home():
    offerings = parse_markdown_files('templates/offerings')
    return render_template('home.html', offerings=offerings)

@app.route('/<title>')
def offering_detail(title):
    try:
        offering = parse_markdown_file(f'templates/offerings/{title}.md')
    except Exception:
        return "Offering not found", 404
    return render_template('offering_detail.html', offering=offering)

def parse_markdown_files(directory):
    markdowner = Markdown()
    offerings = []
    for file in os.listdir(directory):
        if file.endswith('.md'):
            with open(f'{directory}/{file}', 'r') as f:
                post = frontmatter.load(f)
            if 'content' in post:
                post['content'] = markdowner.convert(post.content)  # Access front matter content using .content
            offerings.append(post)
    return offerings

def parse_markdown_file(filepath):
    markdowner = Markdown()
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)
    if 'content' in post:
        post['content'] = markdowner.convert(post.content)  # Access front matter content using .content
    return post

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

