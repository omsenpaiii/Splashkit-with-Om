# Importing flask module from Flask package.
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Intialising App

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" # Intialising Sequel Alchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Creating Database using class for telling Flask what we are storing.

class Todo(db.Model): # Creating our tables columns.
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Creating Routes
@app.route("/", methods=['GET', 'POST']) # If we post by any route we have to provide method
def hello_world():
    if request.method=='POST':
        
        title = request.form['title'] # print("post")
        desc = request.form['desc']

        todo = Todo(title=title, desc = desc)
        db.session.add(todo) # Data will be written into the database successfully.
        db.session.commit()
    
    allTodo = Todo.query.all() # Displaying Todo's
    return render_template('index.html', allTodo = allTodo) # Rendering Html and displaying our Templates

# Creating Post Requests
@app.route("/show") # /show is used to show the todo's
def products():
    allTodo = Todo.query.all() # Printing Todo's
    print(allTodo)
    return "<p>This is products page.</p>"

@app.route('/update/<int:sno>', methods=['GET', 'POST']) # /update is used to edit the todo's
def update(sno):
    if request.method=='POST':
        title = request.form['title'] # print("post")
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() 
        todo.title = title
        todo.desc = desc
        db.session.add(todo) # Data will be written into the database successfully.
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()  # Editing To-do
    return render_template('update.html', todo=todo) 
    

@app.route("/delete/<int:sno>") # /delete is used to complete the todo's and will do so by take S. no.
def delete(sno): #and then deleting it.
    todo = Todo.query.filter_by(sno=sno).first() # Completing Todo's, .first() selecting first record for deleting
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# @app.route("/videos")
# def products():
#     return "<p>This is Videos page.</p>"


# Running our Web App
if __name__ == "__main__":
    app.run(debug=True, port=8000)
