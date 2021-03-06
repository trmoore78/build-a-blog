from flask import Flask, request, redirect, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello1@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        

@app.route('/blog',methods=['GET'])
def blog():
    blog_id = request.args.get('id')
    if blog_id:
        postid = Blog.query.get(blog_id)
        return render_template('display.html',postid=postid)
    
        
@app.route('/newpost',methods=['GET','POST']) 
def newpost():

    new_title_error=""
    new_body_error=""

    if request.method == 'POST':
        new_title = cgi.escape(request.form['title'])
        new_body = cgi.escape(request.form['body'])
        if len(new_title) == 0:
            new_title_error = "Please enter a title for your new post"
            return render_template('post.html',new_title_error=new_title_error,new_body=new_body)
        elif len(new_body) == 0:
            new_body_error = "Please enter a body for your new post"
            return render_template('post.html',new_title=new_title,new_body_error=new_body_error)
        else:
            new_blog = Blog(new_title, new_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={}'.format(new_blog.id))

    elif request.method == 'GET':
        return render_template('post.html')

    

@app.route("/", methods=['GET'])
def index():
    posts = Blog.query.all()
    return render_template('base.html', posts=posts)


if __name__ == '__main__':
    app.run()