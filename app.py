from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.Integer, nullable=False)
  title = db.Column(db.String(200), nullable=False)
  author = db.Column(db.String(200), nullable=False)

with app.app_context():
  db.create_all()

@app.route('/', methods=['GET','POST'])
def home():
  if request.method == 'POST':
    book_isbn = request.form.get('isbn')
    book_title = request.form.get('title')
    book_author = request.form.get('author')
    if book_isbn and book_title and book_author:
      new_book = Book(isbn=book_isbn, title=book_title, author=book_author)
      db.session.add(new_book)
      db.session.commit()

      return redirect(url_for('home'))
  
  column_names = [col for col in Book.__table__.columns.keys() if col != 'id']
  books = Book.query.all()
  return render_template('index.html', books=books, column_names=column_names)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
  book = Book.query.get(book_id)
  if book: 
    db.session.delete(book)
    db.session.commit()
  return redirect(url_for('home'))

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
  book = Book.query.get(book_id)
  if request.method == 'POST':
    new_isbn = request.form['isbn']
    new_title = request.form['title']
    new_author = request.form['author']
    if book:
      book.isbn = new_isbn
      book.title = new_title
      book.author = new_author
      db.session.commit()
    return redirect(url_for('home'))
  else:
    return render_template('edit_book.html', book=book)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8080', debug=True)