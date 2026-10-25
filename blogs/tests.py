from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Blog, Category


class BlogStatusChoicesTest(TestCase):
    def test_status_choices_are_consistent(self):
        status_field = Blog._meta.get_field('status')

        self.assertEqual(status_field.default, 'Draft')
        self.assertEqual(status_field.choices, [('Draft', 'Draft'), ('Published', 'Published')])


class SignupViewTest(TestCase):
    def test_signup_page_displays_registration_form(self):
        response = self.client.get('/signup/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_signup_page_works_without_trailing_slash(self):
        response = self.client.get('/signup')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_valid_signup_creates_user_and_redirects_home(self):
        response = self.client.post('/signup/', {
            'username': 'newmember',
            'password1': 'SafePass!123',
            'password2': 'SafePass!123',
        })

        self.assertRedirects(response, '/')
        self.assertTrue(
            get_user_model().objects.filter(username='newmember').exists()
        )


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="existingmember",
            password="SafePass!123",
        )

    def test_login_page_displays_form_and_signup_link(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, reverse("signup"))

    def test_valid_login_authenticates_user_and_redirects_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": "existingmember", "password": "SafePass!123"},
        )

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_invalid_login_displays_error_without_authenticating(self):
        response = self.client.post(
            reverse("login"),
            {"username": "existingmember", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "existingmember",
                "password": "SafePass!123",
                "next": "https://example.com/",
            },
        )

        self.assertRedirects(response, reverse("home"))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="logoutmember",
            password="SafePass!123",
        )
        self.client.force_login(self.user)

    def test_logout_clears_session_and_redirects_home(self):
        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_rejects_get_requests(self):
        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)


class SearchViewTest(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(username="searchauthor")
        self.category = Category.objects.create(category_name="Search")
        Blog.objects.create(
            title="Django Search",
            slug="django-search",
            category=self.category,
            author=self.author,
            short_description="A guide to search",
            blog_body="Searchable content",
            status="Published",
        )
        Blog.objects.create(
            title="Draft Search",
            slug="draft-search",
            category=self.category,
            author=self.author,
            short_description="A draft guide",
            blog_body="Searchable draft content",
            status="Draft",
        )

    def test_search_url_returns_matching_published_posts(self):
        response = self.client.get("/search", {"keywords": "search"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Search")
        self.assertContains(response, 'value="search"')
        self.assertNotContains(response, "Draft Search")

    def test_search_matches_blog_body(self):
        response = self.client.get("/search", {"keywords": "searchable"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Search")

    def test_empty_search_prompts_for_a_search_term(self):
        response = self.client.get("/search")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a search term")
        self.assertNotContains(response, "Django Search")
