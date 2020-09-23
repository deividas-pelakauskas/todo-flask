from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)


@app.route("/")
def index():
    # show all todos
    task_list = Task.query.all()
    heading = "Tasks to be completed"
    page_description = "These are your tasks that are due to be completed"
    return render_template("home.html", task_list=task_list, title="Tasks", heading=heading, page_description=page_description)


@app.route("/add", methods=["POST"])
def add():
    """
    Add new task

    """
    title = request.form.get("title")
    new_task = Task(title=title, completed=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>")
def update(task_id):
    """
    Update task

    """
    task = Task.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    """
    Delete task

    """
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
