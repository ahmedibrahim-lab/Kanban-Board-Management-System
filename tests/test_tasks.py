import unittest
from app import app, get_db_connection
from datetime import datetime
from werkzeug.security import generate_password_hash

class TaskTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = get_db_connection()
        cls.cursor = cls.conn.cursor()
    
    @classmethod
    def tearDownClass(cls):
        cls.cursor.close()
        cls.conn.close()
    
    def setUp(self):
        query = """
            DELETE FROM kanban_user WHERE name IN ('Task User');
        """
        self.cursor.execute(query)
        self.cursor.execute("INSERT INTO kanban_user (name, password_hash, email) VALUES (%s, %s, %s)",
                            ("Task User", generate_password_hash("taskpassword"), "taskuser@example.com"))
        self.user_id = self.cursor.lastrowid
        self.conn.commit()
    
    def tearDown(self):
        with app.test_client() as client:
            response = client.get('/auth/logout')
            self.assertEqual(response.status_code, 302, "Logout failed, did not redirect.")
        query = """
            DELETE FROM kanban_user WHERE name IN ('Task User');
        """
        self.cursor.execute(query)
        self.conn.commit()
        
    def log_in(self, client):
        # Helper method to log in the user
        response = client.post('/auth/login', data={
            'email': 'taskuser@example.com',
            'password': "taskpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Login failed.")

    def test_create_task(self):
        """Test creating a new task using the create_task_route."""
        with app.test_client() as client:
            self.log_in(client)
            response = client.post('/create_task', data={
                'task_name': 'Test Task',
                'description': 'This is a test task.',
                'priority': 'High',
                'deadline': '2024-12-31',
                'stage': 'To Do',
                'created_by' : self.user_id
            }, follow_redirects=True)

            # Check for successful redirect
            self.assertEqual(response.status_code, 200)

            # Verify the task was created
            self.cursor.execute("SELECT * FROM task WHERE task_name = %s", ("Test Task",))
            task = self.cursor.fetchone()
            self.assertIsNotNone(task, "Failed to create task.")

    def test_update_task_status(self):
        """Test updating task status via the update_status route."""
        # Insert a test task
        self.cursor.execute("INSERT INTO task (task_name, description, priority, deadline, stage, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                            ("Status Test Task", "Update status test", "Medium", "2024-12-31", "To Do", self.user_id))
        task_id = self.cursor.lastrowid
        self.conn.commit()

        with app.test_client() as client:
            self.log_in(client)
            response = client.post('/update_task_status', json={
                'task_id': task_id,
                'new_stage': 'In Progress'
            })

            self.assertEqual(response.status_code, 200)

            # Verify the status was updated
            self.cursor.execute("SELECT stage FROM task WHERE task_id = %s", (task_id,))
            updated_task = self.cursor.fetchone()
            self.assertEqual(updated_task[0], 'In Progress', "Failed to update task status.")
            
    def test_edit_task(self):
        """Test editing a task via edit_task_route."""
        # Insert a test task to edit
        self.cursor.execute("INSERT INTO task (task_name, description, priority, deadline, stage, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                            ("Edit Test Task", "Initial description", "Medium", "2024-12-31", "To Do", self.user_id))
        task_id = self.cursor.lastrowid
        self.conn.commit()

        # New data for updating the task
        updated_data = {
            'task_name': "Updated Test Task",
            'description': "Updated description",
            'priority': "High",
            'deadline': "2025-01-15 09:00:00"
        }

        with app.test_client() as client:
            self.log_in(client)
            
            # Send POST request to edit the task
            response = client.post(f'edit_task/{task_id}', data=updated_data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Verify that the task was updated
            self.cursor.execute("SELECT task_name, description, priority, deadline FROM task WHERE task_id = %s", (task_id,))
            updated_task = self.cursor.fetchone()

            self.assertIsNotNone(updated_task, "Task was not found after edit.")
            self.assertEqual(updated_task[0], updated_data['task_name'], "Task name was not updated.")
            self.assertEqual(updated_task[1], updated_data['description'], "Description was not updated.")
            self.assertEqual(updated_task[2], updated_data['priority'], "Priority was not updated.")
            self.assertEqual(str(updated_task[3]), updated_data['deadline'], "Deadline was not updated correctly.")


    def test_delete_task(self):
        """Test deleting a task via delete_task_route."""
        # Insert a test task to delete
        self.cursor.execute("INSERT INTO task (task_name, description, priority, deadline, stage, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                            ("Delete Test Task", "Description for delete test", "Low", "2024-12-31", "To Do", self.user_id))
        task_id = self.cursor.lastrowid
        self.conn.commit()

        with app.test_client() as client:
            self.log_in(client)
            response = client.post(f'/delete_task/{task_id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Verify the task was deleted
            self.cursor.execute("SELECT * FROM task WHERE task_id = %s", (task_id,))
            task = self.cursor.fetchone()
            self.assertIsNone(task, "Failed to delete task.")

if __name__ == '__main__':
    unittest.main()