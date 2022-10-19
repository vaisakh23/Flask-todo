from flask import Blueprint, render_template, redirect, url_for, flash, request, escape
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegistrationForm
from .models import User, Todo 


views = Blueprint('views', __name__)

@views.route("/", methods= ["GET", "POST"])
def log_in():
	if current_user.is_authenticated:
		return redirect(url_for('views.todo_list'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			flash('Logged in successfully!', category='success')
			login_user(user, remember=form.remember.data)
			return redirect(url_for('views.todo_list'))
	return render_template("login.html", form=form)

@views.route("/signup", methods= ["GET", "POST"])
def sign_up():
	form = RegistrationForm()
	if form.validate_on_submit():
		new_user = User(name=form.name.data, email=form.email.data, 
					password=generate_password_hash(form.password.data))
		db.session.add(new_user)
		db.session.commit()
		flash("Account created!", category='success')
		return redirect(url_for('views.log_in'))
	return render_template("signup.html", form=form)

@views.route("/todo-list", methods=['GET', 'POST'])
@login_required
def todo_list():
	if request.method == "POST":
		new_task = escape(request.form.get('task'))
		if len(new_task.strip())> 0:
			todo = Todo(text=new_task, user_id=current_user.id)
			db.session.add(todo)
			db.session.commit()
			return redirect(url_for('views.todo_list'))
	return render_template("todolist.html")

@views.route("/log-out")
@login_required
def log_out():
	logout_user()
	return redirect(url_for("views.log_in"))

@views.route("/delete-task/<int:todo_id>")
@login_required
def delete_task(todo_id):
	task = Todo.query.get(todo_id)
	if task:
		db.session.delete(task)
		db.session.commit()
	return redirect(url_for('views.todo_list'))
		
@views.route("/update-task", methods=['GET','POST'])
@login_required
def update_task():
	if request.method == "POST":
		id = request.form.get('task_id')
		new_task = request.form.get('task')
		task = Todo.query.get(int(id))
		if task:
			task.text = new_task
			db.session.commit()	
	return redirect(url_for('views.todo_list'))
