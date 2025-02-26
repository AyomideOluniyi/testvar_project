import unittest
from app import app, db
from models import FlashcardSet, FlashCard, Comment, Review, Telemetry

class BasicTests(unittest.TestCase):
    # This method is called before each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    # This method is called after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    # Test for the home route
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to TestVar Flashcards', response.data)

    # Test for creating a new flashcard set
    def test_create_set(self):
        response = self.app.post('/sets/new', data=dict(name='Test Set'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # This will check that the new set name appears in the response
        self.assertIn(b'Test Set', response.data)


class ExtendedTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_sets(self):
        with app.app_context():
            fs = FlashcardSet(name="Test Set")
            db.session.add(fs)
            db.session.commit()
        response = self.app.get('/sets')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Set", response.data)

    def test_delete_set(self):
        with app.app_context():
            fs = FlashcardSet(name="To be deleted")
            db.session.add(fs)
            db.session.commit()
            set_id = fs.id
        response = self.app.delete(f'/sets/{set_id}')
        self.assertEqual(response.status_code, 204)
        response = self.app.get(f'/sets/{set_id}')
        self.assertEqual(response.status_code, 404)

    def test_add_flashcard(self):
        with app.app_context():
            fs = FlashcardSet(name="Flashcard Test Set")
            db.session.add(fs)
            db.session.commit()
            set_id = fs.id
        response = self.app.post(f'/sets/{set_id}/cards/new', data={
            'question': 'What is 2+2?',
            'answer': '4',
            'hidden': 'on'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'What is 2+2?', response.data)

    def test_add_comment(self):
        with app.app_context():
            fs = FlashcardSet(name="Comment Test Set")
            db.session.add(fs)
            db.session.commit()
            set_id = fs.id
        response = self.app.post(f'/set/{set_id}/comment', data={
            'comment': 'Nice set!',
            'author': 'Tester'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nice set!', response.data)

    def test_add_review(self):
        with app.app_context():
            fs = FlashcardSet(name="Review Test Set")
            db.session.add(fs)
            db.session.commit()
            set_id = fs.id
        response = self.app.post(f'/sets/{set_id}/review', json={
            'rating': 5,
            'review_text': 'Excellent!',
            'author': 'Reviewer'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Excellent!', response.data)

    def test_telemetry(self):
        with app.app_context():
            fs = FlashcardSet(name="Telemetry Test Set")
            db.session.add(fs)
            db.session.commit()
            set_id = fs.id
            card = FlashCard(question="Test Q", answer="Test A", set_id=set_id)
            db.session.add(card)
            db.session.commit()
            card_id = card.id
        response = self.app.post('/telemetry', json={
            'flashcard_set_id': set_id,
            'flashcard_id': card_id,
            'event': 'show_answer',
            'duration': 1.2
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Telemetry data recorded', response.data)

    def test_admin_daily_limit(self):
        # Test GET for admin daily limit
        response = self.app.get('/admin/daily_limit')
        self.assertEqual(response.status_code, 200)
        # Test POST to update the daily limit
        response = self.app.post('/admin/daily_limit', data={
            'daily_limit': 50
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            self.assertEqual(app.config['DAILY_LIMIT'], 50)

if __name__ == '__main__':
    unittest.main()
