from flask import Flask, render_template
import os
import frontmatter
import markdown2

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
    offerings = []
    for file in os.listdir(directory):
        if file.endswith('.md'):
            with open(f'{directory}/{file}', 'r') as f:
                post = frontmatter.load(f)
            if 'content' in post:
                post['content'] = markdown2.markdown(post['content'])  # Convert Markdown to HTML
            offerings.append(post)
    return offerings

def parse_markdown_file(filepath):
    with open(filepath, 'r') as f:
        post = frontmatter.load(f)
    if 'content' in post:
        post['content'] = markdown2.markdown(post['content'])  # Convert Markdown to HTML
    return post

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)




