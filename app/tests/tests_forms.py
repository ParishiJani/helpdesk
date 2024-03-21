import unittest
from app import app
from app.forms import (
    LoginForm,
    TicketForm,
    AmendTicketForm,
    DeleteTicketForm,
    RegistrationForm,
    )

class TestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the application context for testing
        cls.app = app  # Create your Flask app instance for testing
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.request_context = cls.app.test_request_context()
        cls.request_context.push()
        cls.app.config['WTF_CSRF_ENABLED'] = False

    @classmethod
    def tearDownClass(cls):
        # Pop the application context
        cls.app_context.pop()
        cls.request_context.pop()

class TestRegistrationForm(TestClass):
    def test_valid_registration(self):
        # Test a valid registration form
        form = RegistrationForm(username='testnamejohndoe',email="testnamejohndoe@user.com", password='strongpassword123', confirm_password='strongpassword123')
        self.assertTrue(form.validate())
        print(form.errors)

    def test_short_username(self):
        # Test form validation with a too short username
        form = RegistrationForm(username='jo', password='strongpassword123')
        self.assertFalse(form.validate())
        self.assertIn('Field must be between 4 and 30 characters long.', form.errors['username'])

    def test_short_password(self):
        # Test form validation with a too short password
        form = RegistrationForm(username='john_doe', password='weak')
        self.assertFalse(form.validate())
        self.assertIn('Field must be at least 6 characters long.', form.errors['password'])

class TestLoginForm(TestClass):
    def test_empty_email(self):
        form = LoginForm(email='', password='testpassword')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.errors['email'])

    def test_invalid_email(self):
        form = LoginForm(email='invalidemail', password='testpassword')
        self.assertFalse(form.validate())
        self.assertIn('Invalid email address.', form.errors['email'])

    def test_short_password(self):
        form = LoginForm(email='test@example.com', password='short')
        self.assertFalse(form.validate())
        self.assertIn('Field must be at least 6 characters long.', form.errors['password'])

class TestTicketForm(TestClass):
    def test_empty_title(self):
        form = TicketForm(title='', description='A valid description.')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.errors['title'])

    def test_long_title(self):
        form = TicketForm(title='t' * 256, description='A valid description.')
        self.assertFalse(form.validate())
        self.assertIn('Field cannot be longer than 255 characters.', form.errors['title'])

class TestAmendTicketForm(TestClass):
    def test_empty_id(self):
        form = AmendTicketForm(id='', title='Valid Title', description='Valid Description')
        self.assertFalse(form.validate())
        self.assertIn('This field is required.', form.errors['id'])

    def test_long_id(self):
        form = AmendTicketForm(id='i' * 101, title='Valid Title', description='Valid Description')
        self.assertFalse(form.validate())
        self.assertIn('Field cannot be longer than 100 characters.', form.errors['id'])

class TestDeleteTicketForm(TestClass):
    def test_valid_deletion(self):
        form = DeleteTicketForm(id='valid_id')
        with open("out.txt", "w") as f:
            f.write(str(form.errors))
        self.assertTrue(form.validate())  # Assuming only ID validation

if __name__ == '__main__':
    unittest.main()