from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from users.models import CustomUser


# Create your tests here.
class RegisterTestCase(TestCase):
    def test_user_account_created(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'Otabek',
                'first_name': 'Otabek',
                'last_name': 'Mikhliev',
                'email': 'mikhlievotabekgmail.com',
                'password': '2001'
            }
        )

    def test_required_fields(self):
        response = self.client.post(
            reverse('login'),
            data={
                "first_name": "Otabek",
                "email": "mikhlievotabekgmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'Otabek',
                'first_name': 'Otabek',
                'last_name': 'Mikhliev',
                'email': 'invalidcom',
                'password': '2001'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="Otabek", first_name="Otabek")
        self.db_user.set_password('2001')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("login"),
            data={
                "username": "Otabek",
                "password": "2001"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("login"),
            data={
                "username": "Otabek1",
                "password": "2001"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="Otabek", password="2001")
        self.client.get(reverse('logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_profile_details(self):
        user = CustomUser.objects.create(username="Otabek",
                                         first_name="Otabek",
                                         last_name="Mikhliev",
                                         email="otabekmikhliev15@gmail.com")
        user.set_password('2001')
        user.save()

        self.client.login(username="Otabek", password="2001")

        response = self.client.get(reverse('profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        user = CustomUser.objects.create(username="Otabek",
                                         first_name="Otabek",
                                         last_name="Mikhliev",
                                         email="otabekmikhliev15@gmail.com")
        user.set_password("2001")
        user.save()

        self.client.login(username="Otabek", password="2001")

        response = self.client.post(
            reverse('profile_edit'),
            data={
                'username': 'Otabek',
                'first_name': 'Otabek',
                'last_name': 'Ibrokhim',
                'email': 'ibro15@gmail.com'
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "Ibrokhim")
        self.assertEqual(user.email, 'ibro15@gmail.com')
        self.assertEqual(response.url, reverse('profile'))