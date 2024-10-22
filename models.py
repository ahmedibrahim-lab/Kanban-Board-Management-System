import mysql.connector
from config import Config

def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
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