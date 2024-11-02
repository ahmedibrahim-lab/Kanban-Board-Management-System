import unittest
from app import app, get_db_connection
from werkzeug.security import generate_password_hash

class AuthTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Establish a database connection before any tests run
        cls.conn = get_db_connection()
        cls.cursor = cls.conn.cursor()
    
    @classmethod
    def tearDownClass(cls):
        # Close the database connection after all tests are done
        cls.cursor.close()
        cls.conn.close()

    def tearDown(self):
        query = """
            DELETE FROM kanban_user WHERE name IN ('Test User', 'Login User');
        """
        self.cursor.execute(query)
        self.conn.commit()

    def test_database_connection(self):
        """Test if the connection to the database is successful."""
        self.cursor.execute("SELECT DATABASE();")
        db_name = self.cursor.fetchone()
        self.assertIsNotNone(db_name, "Database connection failed.")

    def test_user_registration(self):
        with app.test_client() as client:
            response = client.post('/auth/register', data={
                'name' : 'Test User',
                'email': 'testuser@example.com',
                'password': 'testpassword'
            })

        # Verify the user was created
        self.cursor.execute("SELECT * FROM kanban_user WHERE name = %s", ("Test User",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user, "Failed to register user.")

    def test_user_login(self):
        """Test user login."""
        # Insert a test user for logging in
        self.cursor.execute("INSERT INTO kanban_user (name, password_hash, email) VALUES (%s, %s, %s)",
                            ("Login User", generate_password_hash("loginpassword"), "loginuser@example.com"))
        self.conn.commit()

        # Simulate login
        with app.test_client() as client:
            response = client.post('/auth/login', data={
                'email': 'loginuser@example.com',
                'password': "loginpassword"
            })
            self.assertEqual(response.status_code, 302, "Login failed, did not redirect.")

    def test_failed_login(self):
        """Test login with invalid credentials."""
        with app.test_client() as client:
            response = client.post('/auth/login', data={
                'email': 'invaliduser@example.com',
                'password': 'invalidpassword'
            })
            self.assertEqual(response.status_code, 200, "Login succeeded with invalid credentials.")

    def test_user_logout(self):
        """Test user logout."""
        with app.test_client() as client:
            # Log in first
            client.post('/auth/login', data={
                'email': 'loginuser@example.com',
                'password': "loginpassword"
            })

            # Now log out
            response = client.get('/auth/logout')
            self.assertEqual(response.status_code, 302, "Logout failed, did not redirect.")

if __name__ == '__main__':
    unittest.main()
