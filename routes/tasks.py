from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import create_task, get_tasks_by_user, assign_task, get_task_assignments, edit_task, delete_task, update_task_status

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET', 'POST'])
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    tasks = get_tasks_by_user(user_id)  # Fetch all tasks for the user
    
    # Initialize filters with default values
    status = request.args.get('status', '')
    due_date = request.args.get('due_date', '')
    priority = request.args.get('priority', '')

    # Apply filtering only if filters are provided
    filtered_tasks = []
    for task in tasks:
        match = True
        if status and task[5] != status.capitalize():  
            match = False
        if due_date and task[4].date() != due_date:  # Compare date only
            match = False
        if priority and task[3] != priority: 
            match = False
        if match:
            filtered_tasks.append(task)

    # Separate filtered tasks by stage
    todo_tasks = [task for task in filtered_tasks if task[5] == 'To Do']
    in_progress_tasks = [task for task in filtered_tasks if task[5] == 'In Progress']
    done_tasks = [task for task in filtered_tasks if task[5] == 'Done']

    return render_template('kanban.html', todo_tasks=todo_tasks, 
                           in_progress_tasks=in_progress_tasks, 
                           done_tasks=done_tasks,
                           current_status=status,
                           current_priority=priority,
                           current_due_date=due_date)

@tasks_bp.route('/assign_task', methods=['POST'])
def assign_task_to_user():
    task_id = request.form['task_id']
    user_id = request.form['user_id']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    assign_task(task_id, user_id, start_time, end_time)
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/filter_tasks', methods=['GET'])
def filter_tasks():
    return view_tasks()  # Call the same function to handle filtering

# Update task status route
@tasks_bp.route('/update_task_status', methods=['POST'])
def update_status():
    data = request.get_json()
    task_id = data['task_id']
    new_stage = data['new_stage']
    
    # Call the model to update the task status
    update_task_status(task_id, new_stage)
    
    return jsonify({'success': True})

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
