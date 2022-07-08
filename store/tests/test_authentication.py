from django.test import TestCase

from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        self.register_user_url = reverse('register-user')
        self.customer = {
            'username': 'lalita',
            'email': 'lali@gmail.com',
            'password1': 'lalshah11@L',
            'password2': 'lalshah11@L',
            'mobile_no': '+912345676542',
            'age': 34,
            'gender': 'Female'
        }
        self.register_brand_url = reverse('register-brand')
        self.brand = {
            'username': 'ram',
            'email': 'rams1@gmail.com',
            'password1': 'ramshah11@R',
            'password2': 'ramshah11@R',
            'brand': 'ram'
        }

        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

    # check for registering user
    def test_can_register_user(self):
        response = self.client.post(self.register_user_url, self.customer)
        self.assertEqual(response.status_code, 302)

    # check for registering brand
    def test_can_register_brand(self):
        response = self.client.post(self.register_brand_url, self.brand)
        self.assertEqual(response.status_code, 302)


# class LoginTest(BaseTest):
