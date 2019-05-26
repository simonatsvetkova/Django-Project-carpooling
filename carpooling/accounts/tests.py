from django.test import TestCase
from django.test import Client
from .forms import *

# Create your tests here.
class SetUp_Class(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="simonatsvetkova3@gmail.com", password="Spring567", first_name="Simona", last_name='Tsvetkova', username='SimonaTsv3')

class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = RegistrationForm(data={'email': "test18@gmail.com", 'password1': "Spring567", 'password2': 'Spring567', 'first_name': "Simona", 'last_name': 'Tsvetkova', 'username': 'SimonaTsv3'})
        self.assertTrue(form.is_valid())



class User_Views_Test(SetUp_Class):

    def test_home_view(self):
        user_login = self.client.login(email="user@mp.com", password="user")
        self.assertTrue(user_login)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_add_user_view(self):
        response = self.client.get("include url for add user view")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "include template name to render the response")

    # # Invalid Data
    # def test_add_user_invalidform_view(self):
    #     response = self.client.post("include url to post the data given", {'email': "admin@mp.com", 'password': "", 'first_name': "mp", 'phone': 12345678})
    #     self.assertTrue('"error": true' in response.content)
    #
    # # Valid Data
    # def test_add_admin_form_view(self):
    #     user_count = User.objects.count()
    #     response = self.client.post("include url to post the data given", {'email': "user@mp.com", 'password': "user", 'first_name': "user"})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(User.objects.count(), user_count+1)
    #     self.assertTrue('"error": false' in response.content)