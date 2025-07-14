from django.test import TestCase
from .models import Vacation, Likes, Country
from django.core.management import call_command
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
from django.core.exceptions import ValidationError


class VacationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
       
        
        """Set up test data for the test case.

        This method is called with the test database already created and
        the apps ready for testing.

        The method sets up the following data:

        - Loads initial data from initial_data.json
        - Retrieves test user and admin
        - Retrieves passwords for test user and admin
        - Creates a test image
        """

        call_command('loaddata', 'initial_data.json')
        cls.user = User.objects.get(username='testuser@example.com')
        cls.user_password = 'UserPass123'
        cls.admin = User.objects.get(username='admin@example.com')
        cls.admin_password = 'Admin456!'
        img_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(img_io, format="JPEG")
        img_io.seek(0)

        cls.image = SimpleUploadedFile(
            "test_image.jpg",
            img_io.read(),
            content_type="image/jpeg"
)
        cls.country = Country.objects.get(id=1)
        
    def test_regular_user_denied_create_vacation(self):
        
        """
        This test checks that a regular user cannot create a new vacation.

        The test logs in as a regular user, tries to create a new vacation,
        and checks that the response status code is 403 (i.e. forbidden).

        """
        self.client.login(username = self.user.username, password = self.user_password)  # regular user
        response = self.client.post(reverse('add_vacation'), {
            'country': 1,
            'description': 'Vacation in Japan',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        })
        
        self.assertEqual(response.status_code, 403)
    
    def test_admin_can_create_vacation_positive(self):
        
        """
        This test checks that an admin user can create a new vacation.

        The test logs in as the admin user, creates a new vacation, and
        checks that the vacation exists in the database and that the
        response status code is 302 (i.e. a redirect).

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 1,
            'description': 'Vacation in Japan',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        }, format='multipart')
        vacation_exists = Vacation.objects.filter(country=1, description='Vacation in Japan').exists()
        self.assertTrue(vacation_exists)
        self.assertEqual(response.status_code, 302)
    def test_admin_vacation_creation_missing_country(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing country.

        The test logs in as the admin user, creates a new vacation with a
        missing country, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist
        in the database.

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'description': 'wrong vacation',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['country'], ['This field is required.'])
    def test_admin_vacation_creation_with_countr_that_does_not_exist(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a country that does not exist.

        The test logs in as the admin user, creates a new vacation with a
        country that does not exist, and checks that the response status
        code is 200 (i.e. a successful response) and that the vacation does
        not exist in the database.

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 100,
            'description': 'wrong vacation',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=100, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['country'], [f"Select a valid choice. That choice is not one of the available choices."])

    def test_admin_vacation_creation_missing_price(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing price.

        The test logs in as the admin user, creates a new vacation with a
        missing price, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist
        in the database.

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': 'wrong vacation',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=2, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['price'], ['This field is required.'])
    def test_admin_vacation_creation_missing_image(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing image.

        The test logs in as the admin user, creates a new vacation with a
        missing image, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist in
        the database. It also verifies that the form contains an error for the
        missing image field.
        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': 'wrong vacation',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00'
        })
        vacation_exists = Vacation.objects.filter(country=2, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['image'], ['This field is required.'])
    def test_admin_vacation_creation_missing_description(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing description.

        The test logs in as the admin user, creates a new vacation with a
        missing description, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist in
        the database.

        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': '',
            'start_date': '2025-12-01',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=2, description='').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['description'], ['This field is required.'])
    def test_admin_vacation_creation_missing_start_date(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing start_date.

        The test logs in as the admin user, creates a new vacation with a
        missing start_date, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist in
        the database.

        """
        
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': 'wrong vacation',
            'start_date': '',
            'end_date': '2025-12-10',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=2, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['start_date'], ['This field is required.'])

    def test_admin_vacation_creation_missing_end_date(self):
        """
        This test checks that an admin user cannot create a new vacation
        with a missing end_date.

        The test logs in as the admin user, creates a new vacation with a
        missing end_date, and checks that the response status code is 200
        (i.e. a successful response) and that the vacation does not exist in
        the database.

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': 'wrong vacation',
            'start_date': '2025-12-01',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=2, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].errors['end_date'], ['This field is required.'])

    def test_admin_vacation_creation_end_date_before_start_date(self):
        """
        This test checks that an admin user cannot create a new vacation
        with an end_date before the start_date.

        The test logs in as the admin user, creates a new vacation with an
        end_date before the start_date, and checks that the response status
        code is 200 (i.e. a successful response) and that the vacation does
        not exist in the database.

        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('add_vacation'), {
            'country': 2,
            'description': 'wrong vacation',
            'start_date': '2025-12-10',
            'end_date': '2025-12-01',
            'price': '1000.00',
            'image': self.image
        })
        vacation_exists = Vacation.objects.filter(country=2, description='wrong vacation').exists()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(vacation_exists)
        self.assertEqual(response.context['form'].non_field_errors()[0], 'End date must be after start date.')
    def test_admin_cannot_like_vacation(self):
        """
        This test checks that an admin user cannot like a vacation.

        The test logs in as the admin user, attempts to like a vacation,
        and checks that the response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('like_vacation'), {'vacation_id': 1})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Admins are not allowed to do this.', status_code=403)
    def test_admin_cannot_unlike_vacation(self):
        """
        This test checks that an admin user cannot unlike a vacation.

        The test logs in as the admin user, attempts to unlike a vacation,
        and checks that the response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.post(reverse('unlike_vacation'), {'vacation_id': 1})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'Admins are not allowed to do this.', status_code=403)
    
    def test_user_cannot_unlike_vacation_already_unliked(self):
        """
        This test checks that a user cannot unlike a vacation that they have
        already unliked.

        The test logs in as a user, unlikes a vacation, and checks that the
        response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.user.username, password=self.user_password)  # user
        response = self.client.post(reverse('unlike_vacation'), {'vacation_id': 1})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'You haven\'t liked this vacation yet.', status_code=403)

    def test_user_cannot_like_vacation_already_liked(self):
        """
        This test checks that a user cannot like a vacation that they have
        already liked.

        The test logs in as a user, likes a vacation, and checks that the
        response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.user.username, password=self.user_password)  # user
        self.client.post(reverse('like_vacation'), {'vacation_id': 1})
        response = self.client.post(reverse('like_vacation'), {'vacation_id': 1})
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, 'You have already liked this vacation.', status_code=403)
    def test_user_like_vacation_success(self):
        
        """
        This test checks that a user can successfully like a vacation.

        The test logs in as a user, likes a vacation, and checks that the
        response status code is 302 (i.e. a redirect) and that the like is
        recorded in the database.

        """
        
        self.client.login(username=self.user.username, password=self.user_password)  # user
        response = self.client.post(reverse('like_vacation'), {'vacation_id': 1})
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        liked = Likes.objects.filter(user=self.user, vacation_id=1).exists()
        self.assertTrue(liked)
    def test_user_unlike_vacation_success(self):
        
        """
        This test checks that a user can successfully unlike a vacation.

        The test logs in as a user, likes a vacation, unlikes the vacation,
        and checks that the response status code is 302 (i.e. a redirect)
        and that the like is removed from the database.
        """
        self.client.login(username=self.user.username, password=self.user_password)  # user
        self.client.post(reverse('like_vacation'), {'vacation_id': 1})
        response = self.client.post(reverse('unlike_vacation'), {'vacation_id': 1})
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        liked = Likes.objects.filter(user=self.user, vacation_id=1).exists()
        self.assertFalse(liked)
    def test_user_cannot_delete_vacation(self):
        """
        This test checks that a user cannot delete a vacation.

        The test logs in as a user, attempts to delete a vacation, and
        checks that the response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.user.username, password=self.user_password)  # user
        response = self.client.get(reverse('delete_vacation', args=[1]))
        self.assertEqual(response.status_code, 403)
    def test_admin_can_delete_vacation_with_are_you_sure(self):
        """
        This test checks that an admin user can delete a vacation after
        confirming the action.

        The test logs in as the admin user, accesses the delete vacation
        confirmation page to ensure the confirmation message is displayed,
        submits the confirmation, and verifies that the vacation is deleted
        and the response redirects to the home page with a success message.
        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('delete_vacation', args=[1]))
        self.assertContains(response, 'Are you sure you want to delete', status_code=200)
        response = self.client.post(reverse('delete_vacation', args=[1]), {'are_you_sure': 'yes'}, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Vacation.objects.filter(id=1).exists())
        self.assertContains(response, 'Vacation deleted successfully')
    
    def test_admin_canel_delete_vacation(self):
        

        """
        This test checks that an admin user can cancel deleting a vacation.

        The test logs in as the admin user, accesses the delete vacation
        confirmation page to ensure the confirmation message and cancel
        button are displayed, and verifies that the page contains a link
        to the home page.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('delete_vacation', args=[1]))
        self.assertContains(response, 'Are you sure you want to delete', status_code=200)
        cancel_url = reverse('home')
        self.assertContains(response, f'href="{cancel_url}"')

    def test_user_cannot_update_vacation(self):
        """
        This test checks that a user cannot update a vacation.

        The test logs in as a user, attempts to update a vacation, and
        checks that the response status code is 403 (i.e. forbidden).
        """

        self.client.login(username=self.user.username, password=self.user_password)  # user
        response = self.client.get(reverse('update_vacation', args=[1]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',
        'start_date': '2025-12-12',
        'end_date': '2025-12-13',
        'price': '1234.56',
        'image': self.image
    })
        self.assertEqual(response.status_code, 403)


    def test_admin_can_update_vacation_all_fields_success(self):
        
        """
        This test checks that an admin user can update a vacation successfully.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with updated data,
        and verifies that the response redirects to the home page with a
        success message.
        """
        
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',
        'start_date': '2025-12-20',
        'end_date': '2025-12-21',
        'price': '1234.56',
        'image': self.image
        }, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Vacation updated successfully')

    def test_admin_can_update_vacation_with_missing_image_success(self):
        
        """
        This test checks that an admin user can update a vacation successfully
        even if the image is not provided.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with updated data
        without an image, and verifies that the response redirects to the home
        page with a success message.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-12-20',
        'end_date': '2025-12-21',
        'price': '1234.56'
        }, follow=True)
        self.assertTrue(Vacation.objects.filter(description='Attempted update').exists())
        self.assertRedirects(response, reverse('home'))
        self.assertContains(response, 'Vacation updated successfully')
    
    def test_admin_can_update_vacation_with_start_date_in_the_past_success(self):
        
        """
        This test checks that an admin user can update a vacation successfully
        even if the start date is in the past.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with updated data
        with a start date in the past, and verifies that the response redirects
        to the home page with a success message.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',
        'end_date': '2025-07-06',
        'price': '1234.56',
        'image': self.image
        }, follow=True)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Vacation.objects.filter(description='Attempted update').exists())
        self.assertContains(response, 'Vacation updated successfully')

    def test_admin_cannot_update_vacation_without_start_date(self):
        
        
        """
        This test checks that an admin user cannot update a vacation
        without a start date.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form without a start
        date, and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the missing start date field and that the vacation does
        not exist in the database.
        """

        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'end_date': '2025-07-06',
        'price': '1234.56',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'start_date', 'This field is required.')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())
    def test_admin_cannot_update_vacation_without_end_date(self):
        
        """
        This test checks that an admin user cannot update a vacation
        without an end date.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form without an end
        date, and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the missing end date field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',
        'price': '1234.56',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'end_date', 'This field is required.')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())

    def test_admin_cannot_update_vacation_without_price(self):
        
        """
        This test checks that an admin user cannot update a vacation
        without a price.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form without a price,
        and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the missing price field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',
        'end_date': '2025-07-06',
        })        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'price', 'This field is required.')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())

    def test_admin_cannot_update_vacation_with_negative_price(self):
        """
        This test checks that an admin user cannot update a vacation
        with a negative price.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with a negative price,
        and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the negative price field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',
        'end_date': '2025-07-06',
        'price': '-1234.56',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'price','Price must be greater than 0')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())  

    def test_admin_cannot_update_vacation_with_0_price(self):
        """
        This test checks that an admin user cannot update a vacation
        with a price of 0.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with a price of 0,
        and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the 0 price field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',
        'end_date': '2025-07-06',
        'price': '0',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'price', 'Price must be greater than 0')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())
    def test_admin_cannot_update_vacation_with_greater_than_10000_price(self):
        """
        This test checks that an admin user cannot update a vacation
        with a price greater than 10000.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with a price greater
        than 10000, and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the greater than 10000 price field and that the vacation does
        not exist in the database.
        """        
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))        
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',                
        'start_date': '2025-06-20',        
        'end_date': '2025-07-06',                
        'price': '10001',   
        })        
        self.assertEqual(response.status_code, 200)        
        self.assertFormError(response.context['form'], 'price', 'Price must be less than 10000')     
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())

    def test_admint_cannot_update_vacation_with_end_date_before_start_date(self):
        """
        This test checks that an admin user cannot update a vacation
        with an end date before the start date.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with an end date
        before the start date, and verifies that the response status code is 200
        (i.e. the form is re-displayed with errors). It also checks that the
        form contains an error for the end date field and that the vacation
        does not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,
        'description': 'Attempted update',        
        'start_date': '2025-06-20',        
        'end_date': '2025-05-06',        
        'price': '1234.56',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('End date must be after start date.', response.context['form'].non_field_errors())
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())

    def test_admin_cannot_update_vacation_without_description(self):
        """
        This test checks that an admin user cannot update a vacation
        without a description.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form without a description,
        and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the missing description field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,        
        'start_date': '2025-06-20',        
        'end_date': '2025-07-06',        
        'price': '1234.56'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'description', 'This field is required.')
        self.assertFalse(Vacation.objects.filter(description='Attempted update').exists())

    def test_update_vacation_with_description_less_than_10_characters(self):
        """
        This test checks that an admin user cannot update a vacation
        with a description less than 10 characters.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with a description
        less than 10 characters, and verifies that the response status code is 200
        (i.e. the form is re-displayed with errors). It also checks that the
        form contains an error for the description field and that the vacation
        does not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 1,                                        
        'description': 'short',        
        'start_date': '2025-06-20',        
        'end_date': '2025-07-06',        
        'price': '1234.56'
        })        
        self.assertEqual(response.status_code, 200)        
        self.assertFormError(response.context['form'], 'description', 'Description must be at least 10 characters')     
        self.assertFalse(Vacation.objects.filter(description='short').exists())
    
    def test_update_without_country(self):
        
        """
        This test checks that an admin user cannot update a vacation
        without a country.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form without a country,
        and verifies that the response status code is 200 (i.e. the form
        is re-displayed with errors). It also checks that the form contains
        an error for the missing country field and that the vacation does
        not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'description': 'short',        
        'start_date': '2025-06-20',        
        'end_date': '2025-07-06',        
        'price': '1234.56'
        })        
        self.assertEqual(response.status_code, 200)        
        self.assertFormError(response.context['form'], 'country', 'This field is required.')

    def test_admit_cannot_update_with_country_that_does_not_exist(self):
        """
        This test checks that an admin user cannot update a vacation
        with a country that does not exist.

        The test logs in as the admin user, accesses the update vacation page
        to ensure the form is displayed, submits the form with a country
        that does not exist, and verifies that the response status code is 200
        (i.e. the form is re-displayed with errors). It also checks that the
        form contains an error for the country field and that the vacation
        does not exist in the database.
        """
        self.client.login(username=self.admin.username, password=self.admin_password)  # admin user
        response = self.client.get(reverse('update_vacation', args=[1]))
        response = self.client.post(reverse('update_vacation', args=[1]), {
        'country': 100,        
        'description': 'short',        
        'start_date': '2025-06-20',        
        'end_date': '2025-07-06',        
        'price': '1234.56'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'country', 'Select a valid choice. That choice is not one of the available choices.')
        self.assertFalse(Vacation.objects.filter(description='short').exists())
    def test_model_create_vacation_success(self):
        """
        This test checks that a new vacation is created in the database
        when the create_vacation method is called.
        """
        vacation = Vacation.objects.create(
        country = self.country,
        description = 'Vacation in Japan',
        start_date = '2025-08-16',
        end_date = '2025-08-25',
        price = '2000.00',
        image = self.image
        )
        self.assertEqual(vacation.description, 'Vacation in Japan')
        self.assertTrue(Vacation.objects.filter(
        country=self.country,
        description='Vacation in Japan',
        start_date='2025-08-16',
        end_date='2025-08-25',
        price=2000.00
        ).exists())

    def test_add_vacation_nagatives_asserts(self):
        
        """
        This test checks that creating a vacation with invalid data raises
        the appropriate ValidationError.

        It performs several sub-tests:
        - Ensures a negative price raises an error: 'Price must be greater than 0'.
        - Ensures a past start date raises an error: 'Start date must be in the future.'.
        - Ensures an end date before the start date raises an error: 'End date must be after start date.'.
        - Ensures a missing image raises an error: 'Image is required.'.
        - Ensures a short description raises an error: 'Description must be at least 10 characters long.'.
        - Ensures a missing country raises an error: 'Country is required'.
        - Ensures a non-existent country raises an error: 'Country does not exist.'.
        """

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country = self.country,
            description = 'Vacation in Japan',
            start_date = '2025-08-16',
            end_date = '2025-08-25',
            price = '-2000.00',
            image = self.image
            ).full_clean()

        self.assertIn('Price must be greater than 0', str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country = self.country,
            description = 'Vacation in Japan',
            start_date = '2020-08-16',
            end_date = '2020-08-25',
            price = '2000.00',
            image = self.image
            ).full_clean()

        self.assertIn('Start date must be in the future.', str(context.exception))
        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country = self.country,
            description = 'Vacation in Japan',
            start_date = '2025-08-16',
            end_date = '2025-08-15',
            price = '2000.00',
            image = self.image
            ).full_clean()

        self.assertIn('End date must be after start date.', str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country = self.country,
            description = 'Vacation in Japan',
            start_date = '2025-08-16',
            end_date = '2025-08-25',
            price = '2000.00',
            image = None
            ).full_clean()

        self.assertIn('Image is required.', str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country = self.country,
            description = 'Vacation',
            start_date = '2025-08-16',
            end_date = '2025-08-25',
            price = '2000.00',
            image = self.image
            ).full_clean()

        self.assertIn('Description must be at least 10 characters long.', str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            description = 'Vacation in Japan',
            start_date = '2025-08-16',
            end_date = '2025-08-25',
            price = '2000.00',
            image = self.image
            )

        self.assertIn('Country is required', str(context.exception))

        with self.assertRaises(ValidationError) as context:
            Vacation.objects.create(
            country_id = 100,
            description = 'Vacation in Japan',
            start_date = '2025-08-16',
            end_date = '2025-08-25',
            price = '2000.00',
            image = self.image
            )

        self.assertIn('Country does not exist.', str(context.exception))
        
# Create your tests here.
