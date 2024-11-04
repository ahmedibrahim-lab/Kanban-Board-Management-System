from flask import session
import mysql.connector
from config import Config


def user_activity_log(table_name, action_type):
    def function_decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

            user_id = session['user_id']
            user_name = session['user_name']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CALL insert_user_activity_log(%s, %s, %s, %s);
            """, (user_id, user_name, table_name, action_type))
            conn.commit()
            cursor.close()
            conn.close()

        return wrapper
    return function_decorator

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    return connection

# User operations
def create_user(name, email, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kanban_user (name, email, password_hash) 
        VALUES (%s, %s, %s)
    """, (name, email, password_hash))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kanban_user WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Task operations
@user_activity_log('task', 'creating new task')
def create_task(task_name, description, priority, deadline, stage, created_by):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO task (task_name, description, priority, deadline, stage, created_by, created_at, updated) 
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, (task_name, description, priority, deadline, stage, created_by))
    conn.commit()
    cursor.close()
    conn.close()

def get_tasks_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, task_name, description, priority, deadline, stage, created_at, updated 
        FROM task 
        WHERE created_by = %s
    """, (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

@user_activity_log('task', 'update task status')
def update_task_status(task_id, new_stage):
    """Update the status of a task by task_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE task 
        SET stage = %s, updated = NOW() 
        WHERE task_id = %s
    """, (new_stage, task_id))
    conn.commit()
    cursor.close()
    conn.close()

@user_activity_log('task', 'edit task')
def edit_task(task_id, task_name, description, deadline, priority):
    """Edit a task by task_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE task 
        SET task_name = %s, description = %s, deadline = %s, priority = %s, updated = NOW() 
        WHERE task_id = %s
    """, (task_name, description, deadline, priority, task_id))
    conn.commit()
    cursor.close()
    conn.close()

@user_activity_log('task', 'delete task')
def delete_task(task_id):
    """Delete a task by task_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task WHERE task_id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Task assignment operations
def assign_task(task_id, user_id, start_time, end_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO task_assignment (task_id, user_id, start_time, end_time)
        VALUES (%s, %s, %s, %s)
    """, (task_id, user_id, start_time, end_time))
    conn.commit()
    cursor.close()
    conn.close()

def get_task_assignments(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT task_id, start_time, end_time 
        FROM task_assignment 
        WHERE user_id = %s
    """, (user_id,))
    assignments = cursor.fetchall()
    cursor.close()
    conn.close()
    return assignments

def get_task_history(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT stage, changed_at
        FROM task_stage_log
        WHERE task_id = %s
        ORDER BY changed_at DESC
    """
    cursor.execute(query, (task_id,))
    history = cursor.fetchall()
    cursor.close()
    
    history_data = [{"stage": row[0], "date":row[1].strftime('%Y-%m-%d'),"time": row[1].strftime('%H:%M:%S')} for row in history]
    return history_data