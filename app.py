import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    complete = db.Column(db.Boolean, default=False)  # Add default for completeness

# Ensure the database is created and a new Todo item is added
with app.app_context():
    # Remove the database if it exists
    if os.path.exists('yourdatabase.db'):
        os.remove('yourdatabase.db')  # Remove existing database file
    
    db.create_all()  # Create new database tables
    
    # Check if the todo item already exists before adding it
    if not Todo.query.filter_by(title="todo 1").first():
        new_todo = Todo(title="todo 1", complete=False)
        db.session.add(new_todo)
        db.session.commit()

@app.route('/')
def home():
    todo_list = Todo.query.all()  # Query all todos
    print(todo_list)  # Print the list of todos to the console
    return render_template('base.html', todo_list=todo_list)  # Pass the todo_list to the template


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")  # Correct variable name
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Todo with this title already exists.", 400
    return redirect(url_for("home"))
    
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
