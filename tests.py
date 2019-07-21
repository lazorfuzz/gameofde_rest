import unittest
import os
import json
from api import app, populate_db
from database import db
from models import SavedSolution

class UsersTestCase(unittest.TestCase):
    """Tests login and create user"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.test_user = {'username': 'testuser', 'password': 'testpass', 'email': 'test@test.com', 'role': 'standard', 'org_id': 1}
        self.token = 'eyJpZCI6IDIsICJ1c2VybmFtZSI6ICJzdHVkZW50IiwgInJvbGUiOiAiYWRtaW4iLCAib3JnX2lkIjogNCwgImNyZWF0ZWQiOiAiMjAxOS0wNy0yMSAwNTowMDoyMS4zNDkzNjYifQ==.kOPOtfigivgmSzxMhZjiVi0lS3+2CS285IgVjRVxY9c='
        with self.app.app_context():
            # create all tables
            db.create_all()
            populate_db()

    def test_user_creation(self):
        """Test API can create a user (POST)"""
        res = self.client().post('/create_account', data=self.test_user)
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        """Test API can login."""
        res = self.client().post('/login', data={'username': 'student', 'password': 'ist440'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIsNotNone(data['token'])
    
    def test_protected_user_endpoint(self):
        """Test API returns 403 for an edit user request without authorization (PUT)"""
        res = self.client().put('/users/2', data={'password': 'newpass'})
        self.assertEqual(res.status_code, 403)
    
    def test_edit_user(self):
        """Test API can edit a user (PUT)"""
        res = self.client().put('/users/2', data={'password': 'newpass'}, headers={'Authorization': self.token})
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class CaesarTestCase(unittest.TestCase):
    """Tests caesar deciphering endpoint"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.test_cipher = {'cipher': 'Pm ol ohk hufaopun jvumpkluaphs av zhf', 'lang': 'idk'}
        with self.app.app_context():
            # create all tables
            db.create_all()
            populate_db()

    def test_decipher(self):
        """Test API can brute force a cipher (POST)"""
        res = self.client().post('/test_caesar', data=self.test_cipher)
        self.assertEqual(res.status_code, 200)
        self.assertIn('If he had anything confidential to say', res.data.decode())

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class SolutionsTestCase(unittest.TestCase):
    """Tests saved solutions endpoint"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.token = 'eyJpZCI6IDIsICJ1c2VybmFtZSI6ICJzdHVkZW50IiwgInJvbGUiOiAiYWRtaW4iLCAib3JnX2lkIjogNCwgImNyZWF0ZWQiOiAiMjAxOS0wNy0yMSAwNTowMDoyMS4zNDkzNjYifQ==.kOPOtfigivgmSzxMhZjiVi0lS3+2CS285IgVjRVxY9c='
        with self.app.app_context():
            # create all tables
            db.create_all()
            populate_db()
            db.session.add(SavedSolution('Pm ol ohk hufaopun jvumpkluaphs av zhf', 'en', 'If he had anything confidential to say', 2))
            db.session.commit()

    def test_get_saved_solutions(self):
        """Test API can brute force a cipher (GET)"""
        res = self.client().get('/saved_solutions', headers={'Authorization': self.token})
        self.assertEqual(res.status_code, 200)
    
    def test_create_saved_solution(self):
        """Test API can create a saved cipher solution (POST)"""
        res = self.client().post('saved_solutions', data={'cipher': 'jvumpkluaphs', 'solution': 'confidential', 'lang': 'en', 'user_id': 2}, headers={'Authorization': self.token})
        self.assertEqual(res.status_code, 201)
    
    def test_delete_saved_solution(self):
        """Test API can delete a saved cipher solution (DELETE)"""
        res = self.client().delete('saved_solutions/1', headers={'Authorization': self.token})
        self.assertEqual(res.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()