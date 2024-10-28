from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import create_task, get_tasks_by_user, assign_task, get_task_assignments, edit_task, delete_task, update_task_status
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    tasks = get_tasks_by_user(user_id)  # Fetch all tasks for the user
    assignments = get_task_assignments(user_id)

    # Filter parameters
    due_date_str = request.args.get('due_date', '')  # Get the due date as a string
    priority = request.args.get('priority', '')

    # Convert due_date_str to a date object if provided
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()  
        except ValueError:
            due_date = None  # Handle invalid date formats gracefully

    # Apply filtering
    filtered_tasks = []
    for task in tasks:
        match = True
        if due_date and task[4].date() != due_date:  # Compare date objects
            match = False
        if priority and task[3] != priority: 
            match = False
        if match:
            filtered_tasks.append(task)

    # Separate filtered tasks by stage
    todo_tasks = [task for task in filtered_tasks if task[5] == 'To Do']
    in_progress_tasks = [task for task in filtered_tasks if task[5] == 'In Progress']
    done_tasks = [task for task in filtered_tasks if task[5] == 'Done']

    return render_template('kanban.html', 
                           todo_tasks=todo_tasks, 
                           in_progress_tasks=in_progress_tasks, 
                           done_tasks=done_tasks, 
                           assignments=assignments,
                           current_priority=priority,
                           current_due_date=due_date_str)

@tasks_bp.route('/filter_tasks', methods=['GET'])
def filter_tasks():
    return view_tasks()  

# Update task status route
@tasks_bp.route('/update_task_status', methods=['POST'])
def update_status():
    data = request.get_json()
    task_id = data['task_id']
    new_stage = data['new_stage']
    
    # Call the model to update the task status
    update_task_status(task_id, new_stage)
    
    return jsonify({'success': True})

@tasks_bp.route('/create_task', methods=['POST'])
def create_task_route():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    created_by = session['user_id']
    task_name = request.form['task_name']
    description = request.form['description']
    priority = request.form['priority']
    deadline = request.form['deadline']
    stage = request.form['stage']

    # Call the model to create a new task
    create_task(task_name, description, priority, deadline, stage, created_by)

    return redirect(url_for('tasks.view_tasks'))

# Edit task route
@tasks_bp.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task_route(task_id):
    task_name = request.form.get('task_name')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    priority = request.form.get('priority')

    # Call the model to edit the task
    edit_task(task_id, task_name, description, deadline, priority)

    return redirect(url_for('tasks.view_tasks'))

# Delete task route
@tasks_bp.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    # Call the model to delete the task
    delete_task(task_id)

    return jsonify({'success': True})
