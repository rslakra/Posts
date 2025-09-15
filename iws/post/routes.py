#
# Author: Rohtash Lakra
# Reference - https://realpython.com/flask-blueprint/
#
import json
import time
from io import BytesIO

from flask import current_app, render_template, request, redirect, send_file

from post.v1 import bp as bp_v1_posts
from rest.post.schema import Document


@bp_v1_posts.get("/")
def index():
    """Load Index Page"""
    posts = [
        {
            "title": "Are blogs important for businesses?",
            "description": "Blogs are an important part of a company’s content strategy, as they can communicate the features and benefits of a product or service.",
            "author": "Rohtash",
            "posted_on": "2024-10-13T00:20:27.466337"
        },
        {
            "title": "How should you format a blog post?",
            "description": "A blog post should be formatted in a way that leads to increased readership and interest. Beginning with an attention-grabbing headline, a well-formatted blog post should also feature relatively brief sentences that convey ideas quickly. The post should also include subheads or section heads, helping readers to quickly understand the message or skip to sections that are more interesting to them. Additionally, photos and other graphics can increase readership, interest, and SEO rankings across search engines.",
            "author": "R. Lakra",
            "posted_on": "2024-10-23T00:40:21.466337"
        }
    ]

    context = {
        'strftime': time.strftime
    }

    current_app.logger.debug(f"posts={json.dumps(posts)}")
    return render_template("post/index.html", posts=posts, **context)


@bp_v1_posts.route('/create', methods=['GET', 'POST'])
def create():
    """Load Create/Add Post Page"""
    if request.method == 'POST':
        body = request.get_json()
        print(f"body={body}")
        return redirect('/')

    """Render Add Post Page"""
    return render_template("post/create.html")


@bp_v1_posts.route('/upload', methods=['GET', 'POST'])
def upload():
    print(f"request.method={request.method}")
    if request.method == 'POST':
        file = request.files['file']
        file_data = file.read()
        # post = Post(title=file.filename, author=file.filename)
        # attachment = Attachment(post=post, filename=file.filename, data=file_data)
        # post.addAttachment(attachment)
        # connector.save(post)
        document = Document(filename=file.filename, data=file_data)
        # connector.save(document)
        upload_metadata = {
            "message": f'Uploaded: {file.filename}'
        }
        # return f'Uploaded: {file.filename}'
        return render_template('post/index.html', upload_metadata=upload_metadata)

    return render_template('post/upload_file.html')


@bp_v1_posts.route('/download/<upload_id>')
def download(upload_id):
    document = Document.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(document.data), download_name=document.filename, as_attachment=True)
