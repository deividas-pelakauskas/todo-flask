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
    return render_template("base.html", task_list=task_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title, completed=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
