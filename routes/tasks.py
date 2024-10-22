from flask import Blueprint, render_template, request, redirect, url_for, session
from models import create_task, get_tasks_by_user, assign_task, get_task_assignments

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET', 'POST'])
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    
    if request.method == 'POST':
        task_name = request.form['task_name']
        description = request.form['description']
        priority = request.form['priority']
        deadline = request.form['deadline']
        stage = request.form['stage']
        create_task(task_name, description, priority, deadline, stage, user_id)
        return redirect(url_for('tasks.view_tasks'))
    tasks = get_tasks_by_user(user_id)
    assignments = get_task_assignments(user_id)
    return render_template('kanban.html', tasks=tasks, assignments=assignments)

@tasks_bp.route('/assign_task', methods=['POST'])
def assign_task_to_user():
    task_id = request.form['task_id']
    user_id = request.form['user_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    assign_task(task_id, user_id, start_time, end_time)
    return redirect(url_for('tasks.view_tasks'))