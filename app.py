from flask import Flask, render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# ✅ Make sure todo.db is created in the same folder as app.py    Created a database db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):                                             # contents of the database
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:                                    # display the following values in table
        return f"{self.sno} - {self.title}"

# CRUD - CREATE READ UPDATE DELETE 
@app.route("/products")
def products():
    # allTodo = Todo.query.all()
    # print(allTodo)                                                 # prints because of repr function in Todo
    return "<p>This is Products page</p>"

# Home page
@app.route("/", methods=['GET','POST'])                           # first thing after going to home page
def hello_world(): 
    if request.method == "POST":                                  # used for submitting the button
        title = request.form['title']
        desc = request.form['desc']
        todo= Todo(title=title,desc=desc)  
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()                                     # jinja2 is a templating engine
    return render_template('index.html',allTodo=allTodo)           # run the html command of bootstrap
                              
# update route
@app.route('/update/<int:sno>', methods=['GET','POST'])                                              # update file
def update(sno):
    if request.method=='POST':
        title = request.form['title']                                # store new title in title
        desc = request.form['desc']                                  # store new desc in desc
        todo= Todo.query.filter_by(sno=sno).first()                  # get the todo which needs to be updated    
        todo.title= title                                            # update the todo
        todo.desc= desc
        db.session.add(todo)                                         # add the todo to database and commit
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()                       # finds the query with given sno                                                
    return render_template('update.html',todo=todo)                  # when you first click on update, these two statements are executed

# delete record
@app.route('/delete/<int:sno>')                                              # delete file
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()                                # finds the query with given sno
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    if not os.path.exists(os.path.join(basedir, "todo.db")):       # if the database does not exists, then create a database
        with app.app_context():
            db.create_all()
            print("✅ Database created successfully!")

    app.run(debug=True, port=8000)                                 # run the database

 

