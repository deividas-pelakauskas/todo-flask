from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime)


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        filter_task = request.form.get('filter-tasks')
        if filter_task == "Deadline":
            task_list = Task.query.order_by(Task.deadline).all()
        else:
            task_list = Task.query.all()

    except:
        task_list = Task.query.all()
    heading = "Tasks to be completed"
    page_description = "These are your tasks that are due to be completed"
    #  Check if there is any due tasks
    due_tasks = tasks_exist()
    return render_template("home.html", task_list=task_list, title="Tasks", heading=heading,
                           page_description=page_description, due_tasks=due_tasks)


@app.route("/completed")
def completed():
    # show completed tasks
    task_list = Task.query.all()
    heading = "Completed tasks"
    page_description = "These are your tasks that are already completed. You can also add new tasks from here."
    return render_template("completed.html", task_list=task_list, title="Completed tasks", heading=heading,
                           page_description=page_description)


@app.route("/add", methods=["POST"])
def add():
    """Add new task"""
    title = request.form.get("title")
    # Convert date which is in String format to datetime
    deadline = datetime.strptime(request.form.get("deadline"), '%Y-%m-%d')
    new_task = Task(title=title, deadline=deadline, completed=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>")
def update(task_id):
    """Update task action"""
    task = Task.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    """Delete task action"""
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>")
def edit_task(task_id):
    """Edit task page"""
    task = Task.query.filter_by(id=task_id).first()
    task_title = task.title
    task_deadline = task.deadline
    heading = "Edit task"
    page_description = "You are editing a task. You can also add task from this page"
    return render_template("edit.html", task_id=task_id, task_title=task_title, task_deadline=task_deadline,
                           title="Edit task", heading=heading,
                           page_description=page_description)


@app.route("/edit-task/<int:task_id>", methods=["POST"])
def edit_task_action(task_id):
    """Edit task function to do the actual editing on the back-end"""
    title = request.form.get("title")
    deadline = request.form.get("deadline")
    task = Task.query.filter_by(id=task_id).first()
    task.title = title
    task.deadline = deadline
    db.session.commit()
    return redirect(url_for("index"))


@app.template_filter('formatdatetime')
def format_datetime(date, format="%d/%m/%Y"):
    """Format a date time to DAY/MONTH/YEAR (Bootstrap date input field comes as YYYY-MM-DD. Date is not required
    field """
    if date is None:
        return ""
    try:
        return date.strftime(format)
    except:
        return ""


def tasks_exist():
    """
    To check if there is any due tasks at all

    :return: Bolean value - true means that there are some due tasks
    """
    if Task.query.filter_by(completed=False).count() > 0:
        return True
    else:
        return False


if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
    app.run(debug=True)
