import unittest

from app import create_app, db
from app.utils import check_answer
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    

class TestIndexPage(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        tester = self.app.test_client()    
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_redirect(self):
        tester = self.app.test_client()    
        response = tester.post('/', data=dict(total='0', username='john_doe'))
        self.assertEqual(response.status_code, 302)


class TestWordManagement(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_words(self):
        tester = self.app.test_client()
        response = tester.get('words')
        self.assertEqual(response.status_code, 200)

    def test_add_word(self):
        tester = self.app.test_client()

        response = tester.get('words')
        self.assertFalse(b'bagoly' in response.data)

        response = tester.post('word/create', data=dict(value='bagoly'), follow_redirects=True)
        self.assertTrue(b'bagoly' in response.data)

    def test_delete_word(self):
        tester = self.app.test_client()
        
        response = tester.get('words')
        self.assertFalse(b'bagoly' in response.data)
        
        response = tester.post('word/create', data=dict(value='bagoly'), follow_redirects=True)
        self.assertTrue(b'bagoly' in response.data)
        
        # TODO: Find a proper way to get the newly created word_id
        response = tester.post('word/1/delete', follow_redirects=True)
        self.assertFalse(b'bagoly' in response.data)

    def test_add_invalid_word(self):
        tester = self.app.test_client()
        
        response = tester.post('word/create', data=dict(value='tesztfeladat'), follow_redirects=True)
        self.assertFalse(b'tesztfeladat' in response.data)

    def test_add_duplicate_word(self):
        tester = self.app.test_client()

        response = tester.get('words')
        self.assertFalse(b'bagoly' in response.data)
        
        response = tester.post('word/create', data=dict(value='bagoly'), follow_redirects=True)
        self.assertTrue(b'bagoly' in response.data)
        
        response = tester.post('word/create', data=dict(value='bagoly'), follow_redirects=True)
        self.assertEqual(response.data.count(b'bagoly'), 1)


class TestCheckAnswer(unittest.TestCase):
    def test_is_correct_valid_success(self):
        # Right spelling, user answer successfully
        question = {'q':'bagoly', 'a': 'bagoly', 'qm': 'is_correct'}
        value = check_answer(question, 'yes')
        self.assertTrue(value)

    def test_is_correct_valid_failed(self):
        # Right spelling, user answer unsuccessfully
        question = {'q': 'bagoly', 'a': 'bagoly', 'qm': 'is_correct'}
        value = check_answer(question, 'no')
        self.assertFalse(value)

    def test_is_correct_invalid_success(self):
        # Wrong spelling, user answer successfully
        question = {'q': 'bagoj', 'a': 'bagoly', 'qm': 'is_correct'}
        value = check_answer(question, 'no')
        self.assertTrue(value)

    def test_is_correct_invalid_failed(self):
        # Wrong spelling, user answer unsuccessfully
        question = {'q': 'bagoj', 'a': 'bagoly', 'qm': 'is_correct'}
        value = check_answer(question, 'yes')
        self.assertFalse(value)

    def test_fill_empty_success(self):
        # User answer successfully
        question = {'q':'bago_', 'a': 'bagoly', 'qm': 'fill_empty'}
        value = check_answer(question, 'ly')
        self.assertTrue(value)

    def test_fill_empty_failed(self):
        # User answer unsuccessfully
        question = {'q':'bago_', 'a': 'bagoly', 'qm': 'fill_empty'}
        value = check_answer(question, 'j')
        self.assertFalse(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
