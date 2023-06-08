from flask import Flask, render_template
import frontmatter
import os
import mistune

app = Flask(__name__)
markdown = mistune.create_markdown()

@app.route('/')
def home():
    tiles = []
    for filename in os.listdir('offerings'):
        if filename.endswith('.md'):
            with open(f'offerings/{filename}') as f:
                post = frontmatter.load(f)
                tiles.append({
                    'title': post['TITLE'],
                    'summary': post['SUMMARY'],
                    'icon': post['ICON'],
                    'url': filename[:-3]  # remove .md
                })
    return render_template('home.html', tiles=tiles)

@app.route('/<name>')
def offering(name):
    with open(f'offerings/{name}.md') as f:
        post = frontmatter.load(f)
        post.content = markdown(post.content)
        return render_template('offering.html', post=post)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
