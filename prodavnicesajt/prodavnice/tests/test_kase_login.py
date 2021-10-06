from django.test import TestCase, Client
from django.urls import reverse
from ..management.commands.popuni_bazu import Command


# Simple test suite that valid behaviour of auth login
class KaseLoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # prepare test db for this test suite
        Command().handle()

    def setUp(self) -> None:
        # instantiate client for each test
        self.client = Client()

    def test_successful_login(self):
        credentials = {'uname': 'user1', 'psw': 'user1'}
        # follow=True says that eventual redirections are considered and followed
        response = self.client.post(reverse('kase_login'), credentials, follow=True)
        # after the successful login, the user is redirected to the page that shows cash desks
        self.assertEqual(response.status_code, 200)
        self.assertTrue('kase' in response.context)
        self.assertEqual(len(response.context['kase']), 3)

    def test_successful_login_forbidden_access(self):
        credentials = {'uname': 'user2', 'psw': 'user2'}
        # follow=True says that eventual redirections are considered and followed
        response = self.client.post(reverse('kase_login'), credentials, follow=True)
        # The user is not authorized to access to the list of cash desks.
        self.assertEqual(response.status_code, 403)

    def test_unsuccessful_login(self):
        credentials = {'uname': 'user3', 'psw': 'user3'}
        # follow=True says that eventual redirections are considered and followed
        response = self.client.post(reverse('kase_login'), credentials, follow=True)
        # assert that the error message is going to be shown
        self.assertTrue('greska_login' in response.context)
        self.assertEqual(response.context['greska_login'], True)

    def test_sucessful_logout(self):
        self.client.login(username='user1', password='user1')
        response = self.client.get(reverse('kase_logout'), follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual((reverse('index'), 302), response.redirect_chain[0])
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_logout(self):
        response = self.client.get(reverse('kase_logout'))
        self.assertEqual(response.status_code, 403)
