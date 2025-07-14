from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.
class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.

        This method is called with the test database already created and
        the apps ready for testing.

        The method sets up the following data:

        - Loads initial data from initial_data.json
        - Retrieves test user and admin
        - Retrieves passwords for test user and admin
        """
        call_command('loaddata', 'initial_data.json')
        cls.user = User.objects.get(username='testuser@example.com')
        cls.user_password = 'UserPass123'
        cls.admin = User.objects.get(username='admin@example.com')
        cls.admin_password = 'Admin456!'

        super().setUpTestData()

    def test_user(self):
        """
        This test checks that the test user is correctly set up.

        The test checks the following:

        - The username is 'testuser@example.com'
        - The first name is 'Test'
        - The last name is 'User'
        - The email is 'testuser@example.com'
        - The user is not a super user
        - The user is not a staff member
        - The user is active

        """
        pass
        self.assertEqual(self.user.username, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_active, True)
    def test_admin(self):
        """
        This test checks that the admin user is correctly set up.

        The test checks the following:

        - The username is 'admin@example.com'
        - The first name is 'Admin'
        - The last name is 'User'
        - The email is 'admin@example.com'
        - The user is not a super user
        - The user is a staff member
        - The user is active

        """
        self.assertEqual(self.admin.username, 'admin@example.com')
        self.assertEqual(self.admin.first_name, 'Admin')
        self.assertEqual(self.admin.last_name, 'User')
        self.assertEqual(self.admin.email, 'admin@example.com')
        self.assertEqual(self.admin.is_superuser, True)
        self.assertEqual(self.admin.is_staff, True)
        self.assertEqual(self.admin.is_active, True)

    def test_user_password(self):
        """
        This test checks that the password for the test user is correct.

        The test checks the following:

        - The password for the test user is 'UserPass123'

        """
        self.assertEqual(self.user.check_password(self.user_password), True)

    def test_admin_password(self):
        """
        This test checks that the password for the admin user is correct.

        The test checks the following:

        - The password for the admin user is 'Admin456!'

        """
        self.assertEqual(self.admin.check_password(self.admin_password), True)

    def test_user_login(self):
        
        """
        This test checks that a user can successfully log in.

        The test checks the following:

        - The test user can log in with their username and password
        - The response redirects to the home page with a status code of 302
        - The response status code is 200

        """
        
        login_success = self.client.login(username=self.user.username, password=self.user_password)
        self.assertTrue(login_success)
        response = self.client.post(reverse('login'), {'username': self.user.username, 'password': self.user_password}, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        self.assertContains(response, 'awaits you,')
        self.assertContains(response, self.user.first_name)

    def test_admin_login(self):
        """
        This test checks that an admin user can successfully log in.

        The test checks the following:

        - The admin user can log in with their username and password
        - The response redirects to the home page with a status code of 302
        - The response status code is 200

        """
        login_success = self.client.login(username=self.admin.username, password=self.admin_password)
        self.assertTrue(login_success)
        response = self.client.post(reverse('login'), {'username': self.admin.username, 'password': self.admin_password}, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        self.assertContains(response, 'awaits you,')
        self.assertContains(response, self.admin.first_name)
        self.assertContains(response, 'Add Vacation')

    def test_user_login_failure(self):
        """
        This test checks that a user cannot log in with incorrect credentials.

        The test checks the following:

        - The user cannot log in with incorrect username and password
        - The response status code is 200

        """
        login_success = self.client.login(username='incorrect_username', password='incorrect_password')
        self.assertFalse(login_success)
        response = self.client.post(reverse('login'), {'username': 'incorrect@username.com', 'password': 'incorrect_password'}, follow=True)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive')

        self.assertEqual(response.status_code, 200)


    def test_signup(self):
        """
        This test checks that a new user can be successfully signed up.

        The test checks the following:

        - The user is redirected to the login page with a status code of 302
        - The response status code is 200
        - A user with the given email exists in the database

        """
        
        response = self.client.post(reverse('signup'), {'email': 'email@email.com','first_name': 'first', 'last_name': 'last','password1': 'newpassword232323', 'password2': 'newpassword232323'})
        print(response.content)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        self.assertTrue(User.objects.filter(email='email@email.com').exists())

    def test_signup_not_unique_email(self):
        """
        This test checks that a user cannot sign up with an email that is already in the database.

        The test checks the following:

        - The response contains the message 'Email already exists'

        """
        response = self.client.post(reverse('signup'), {'email': 'testuser@example.com','first_name': 'first', 'last_name': 'last','password1': 'newpassword232323', 'password2': 'newpassword232323'})
        self.assertContains(response, 'Email already exists')

    def test_signup_invalid_email(self):
        """
        This test checks that a user cannot sign up with an invalid email address.

        The test checks the following:

        - The response contains the message 'Enter a valid email address.'

        """
        response = self.client.post(reverse('signup'), {'email': 'invalid_email','first_name': 'first', 'last_name': 'last','password1': 'newpassword232323', 'password2': 'newpassword232323'})
        self.assertContains(response, 'Enter a valid email address.')

    def test_signup_passwords_do_not_match(self):
        """
        This test checks that a user cannot sign up with passwords that do not match.

        The test checks the following:

        - The response contains the message 'The two password fields didn’t match.'

        """
        response = self.client.post(reverse('signup'), {'email': 'email@email.com','first_name': 'first', 'last_name': 'last','password1': 'newpassword232323', 'password2': 'wrongpassword'})
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_signup_password_too_short(self):
        """
        This test checks that a user cannot sign up with a password that is too short.

        The test checks the following:

        - The response contains the message 'Your password is too short. It must contain at least 8 characters.'

        """
        response = self.client.post(reverse('signup'), {'email': 'email@email.com','first_name': 'first', 'last_name': 'last','password1': 'short', 'password2': 'short'})
        self.assertContains(response, 'This password is too short. It must contain at least 8 characters.')


    