import unittest
from app import app, db
from models import FlashcardSet

class BasicTests(unittest.TestCase):
    # Thes method is called before each test
    def setUp(self):
        app.config['TESTING'] = True
        # this wil Use an in-memory SQLite database for tests
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # This method is called after each test
    def tearDown(self):
        # Drop the database tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Test the home route
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to TestVar Flashcards!', response.data)

    # Test creating a new flashcard set
    def test_create_set(self):
        response = self.app.post('/sets/new', data=dict(name='Test Set'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        #  this will check that the new set name appears in the response
        self.assertIn(b'Test Set', response.data)

if __name__ == '__main__':
    unittest.main()
