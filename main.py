from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


@app.route('/')
def home():
    books = db.session.query(Book).all()
    return render_template("index.html", books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        book_author = request.form.get('book_author')
        book_rating = request.form.get('rating')
        new_book = Book(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        new_rating = request.form.get('new_rating')
        book.rating = float(new_rating)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', book=book)


@app.route('/delete/<int:book_id>')
def delete(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
