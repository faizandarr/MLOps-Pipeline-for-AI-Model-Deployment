import unittest
import json
from app import app, db, User

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

        # Set up the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        response = self.app.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

    def test_login(self):
        # First, create a user
        self.app.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')

        # Then, try to log in
        response = self.app.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_predict(self):
        # First, create a user and log in
        self.app.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        login_response = self.app.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        user_id = json.loads(login_response.data)['user_id']

        # Then, make a prediction
        response = self.app.post('/predict', data=json.dumps({
            'user_id': user_id,
            'humidity': 50,
            'windSpeed': 10
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'temperature', response.data)

    def test_logout(self):
        # First, create a user and log in
        self.app.post('/signup', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.app.post('/login', data=json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')

        # Then, log out
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout successful', response.data)

if __name__ == '__main__':
    unittest.main()