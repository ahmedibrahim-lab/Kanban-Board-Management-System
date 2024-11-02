from flask import Flask, redirect, url_for
from routes.auth import auth_bp
from routes.tasks import tasks_bp
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config.Config')

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Register the blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.register'))

@app.route('/test_db')
def test_db():
    conn = None
    cursor = None
    try:
        conn = get_db_connection() 
        cursor = conn.cursor() 
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        return f"Connected to database: {db_name[0]}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        
if __name__ == '__main__':
    app.run(debug=True)