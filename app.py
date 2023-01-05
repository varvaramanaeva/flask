from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import DateTime, Column, Integer, String, Text
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inform.db'
db = SQLAlchemy(app)


class InformationPiece(db.Model):
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    articles = InformationPiece.query.order_by(InformationPiece.date.desc()).all()
    return render_template('index.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def post(id):
    if request.method == "GET":
        article = InformationPiece.query.get(id)
        return render_template('post.html', article=article)
    elif request.method == "PUT":
        return redirect(f'/post/{id}/update')
    else:
        return redirect(f'/post/{id}/delete')


@app.route('/post/<int:id>/delete')
def post_delete(id):
    article = InformationPiece.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('post.html', article=article)


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = InformationPiece.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:

        return render_template('post_update.html', article=article)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = InformationPiece(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

