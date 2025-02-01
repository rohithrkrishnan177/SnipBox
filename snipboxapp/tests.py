from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Tag, Snippet


# Test for Tag and Snippet Models
from .serializers import SnippetSerializer, SnippetViewSetSerializer


class TagAndSnippetTestCase(TestCase):
    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_tag_creation(self):
        # Create a new tag and verify if it's created successfully
        tag = Tag.objects.create(tag_title="TEST")
        self.assertEqual(tag.tag_title, "TEST")
        self.assertTrue(Tag.objects.filter(tag_title="TEST").exists())

    def test_snippet_creation(self):
        # Create a new snippet and verify if it's created successfully
        tag = Tag.objects.create(tag_title="WORK")
        snippet = Snippet.objects.create(
            snippet_title="Test Snippet",
            note="This is a test note.",
            created_by=self.user
        )
        snippet.tags.add(tag)

        self.assertEqual(snippet.snippet_title, "Test Snippet")
        self.assertEqual(snippet.created_by, self.user)
        self.assertTrue(snippet.tags.filter(tag_title="WORK").exists())


class CreateUserViewTestCase(APITestCase):
    def setUp(self):
        # Create a sample admin user for authentication
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpassword', is_staff=True
        )
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.url = '/api/create-user/'

    def test_create_user(self):
        # Define the data to create a new user, including the password
        data = {
            'username': 'rohith',
            'email': 'newuser@example.com',
            'first_name': 'ROHITH',
            'last_name': 'KRISHNAN',
            'password': 'password123'  # Include password
        }

        # Make a POST request to create a new user
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  # Include the admin token in the headers
        )

        # Print the response content for debugging
        print(response.status_code)
        print(response.data)

        # Check if the status is HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the response contains the created user data
        self.assertEqual(response.data["username"], "rohith")
        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertEqual(response.data["first_name"], "ROHITH")
        self.assertEqual(response.data["last_name"], "KRISHNAN")

    def test_create_user_without_authentication(self):
        # Define the data to create a new user
        data = {
            'username': 'rohith',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }

        # Make a POST request to create a new user without authentication
        response = self.client.post(self.url, data, format='json')

        # Check if the status is HTTP 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check if the response contains an appropriate error message
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_create_user_with_payload(self):
        # Define the payload for creating a new user
        payload = {
            "username": "newuser8",
            "password": "password123",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User"
        }

        # Make a POST request to create a new user with the payload
        response = self.client.post(
            self.url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  # Include the admin token in the headers
        )

        # Check if the status is HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the created user data
        self.assertEqual(response.data["username"], "newuser8")
        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertEqual(response.data["first_name"], "New")
        self.assertEqual(response.data["last_name"], "User")


class CreateSnippetAPITestCase(APITestCase):
    def setUp(self):
        # Create a sample admin user for authentication
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpassword'
        )
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.url = '/api/snippets/create/'

    def test_create_snippet(self):
        # Define the data for creating a snippet
        data = {
            'snippet_title': 'Sample Snippet',
            'note': 'This is a test snippet.',
            'tags': ['test', 'api']  # Assuming you have a tags field in the Snippet model
        }

        # Make a POST request to create a new snippet
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        print(response.data)

        # Check if the status is HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the created snippet data
        self.assertEqual(response.data["snippet_title"], "Sample Snippet")
        self.assertEqual(response.data["note"], "This is a test snippet.")

        # Check that the response contains the correct tag details
        self.assertEqual(len(response.data["tag_details"]), 2)  # Ensure there are 2 tags
        self.assertEqual(response.data["tag_details"][0]["tag_title"], "test")
        self.assertEqual(response.data["tag_details"][1]["tag_title"], "api")

    def test_create_snippet_without_authentication(self):
        # Define the data for creating a snippet
        data = {
            'snippet_title': 'Unauthorized Snippet',
            'note': 'This snippet should fail.',
            'tags': ['test']
        }

        # Make a POST request without authentication
        response = self.client.post(self.url, data, format='json')

        # Check if the status is HTTP 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check if the response contains the expected error message
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")


class TagViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a sample admin user for authentication
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpassword'
        )
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.url = '/api/tags/'  # URL to the TagViewSet

    def test_create_tag(self):
        # Define the data for creating a tag
        data = {
            'tag_title': 'tag26'
        }

        # Make a POST request to create a new tag
        response = self.client.post(
            self.url,
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        # Check if the status is HTTP 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response contains the correct tag_title
        self.assertEqual(response.data["tag_title"], "tag26")

    def test_create_tag_without_authentication(self):
        # Define the data for creating a tag
        data = {
            'tag_title': 'tag27'
        }

        # Make a POST request without authentication
        response = self.client.post(self.url, data, format='json')

        # Check if the status is HTTP 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check if the response contains the expected error message
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")


class SnippetOverviewAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create a test snippet associated with the user
        self.snippet = Snippet.objects.create(
            snippet_title="Test Snippet",
            note="This is a test note",
            created_by=self.user  # Ensure the created_by field is populated
        )

        # Initialize API client
        self.client = APIClient()

    def test_snippet_overview(self):
        """Test retrieving the snippet overview with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/snippets/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Response JSON:", data)  # Debugging output

        self.assertIn("snippets", data)  # Ensure "snippets" key exists
        self.assertTrue(len(data["snippets"]) > 0, "No snippets found in response")

        # Extract snippet URLs (or other fields you expect)
        snippet_urls = [snippet.get("url", "") for snippet in data["snippets"]]
        print("Extracted snippet URLs:", snippet_urls)

        # Ensure at least one snippet has a non-empty URL
        self.assertTrue(any(url for url in snippet_urls if url), "All snippet URLs are empty")

    def test_snippet_overview_without_authentication(self):
        """Test retrieving the snippet overview without authentication"""
        response = self.client.get("/api/snippets/")
        self.assertEqual(response.status_code, 401)  # Should return Unauthorized

    def tearDown(self):
        self.client.logout()


class SnippetDetailAPITestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a tag
        self.tag = Tag.objects.create(tag_title='django')

        # Create a snippet
        self.snippet = Snippet.objects.create(
            snippet_title='Test Snippet',
            note='This is a test snippet',
            created_by=self.user
        )
        self.snippet.tags.add(self.tag)

        # URL for the snippet detail
        self.url = reverse('snippet-detail', kwargs={'pk': self.snippet.id})

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_get_snippet_detail(self):
        # Make a GET request to the snippet detail endpoint
        response = self.client.get(self.url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data matches the expected data
        expected_data = SnippetSerializer(self.snippet).data
        self.assertEqual(response.data, expected_data)

        # Check that the tag_details are included in the response
        self.assertIn('tag_details', response.data)
        self.assertEqual(len(response.data['tag_details']), 1)
        self.assertEqual(response.data['tag_details'][0]['tag_title'], 'django')


class SnippetModelTestCase(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.tag1 = Tag.objects.create(tag_title="Django")
        self.tag2 = Tag.objects.create(tag_title="Python")

        self.snippet = Snippet.objects.create(
            snippet_title="Test Snippet",
            note="This is a test note.",
            created_by=self.user
        )
        self.snippet.tags.add(self.tag1, self.tag2)

    def test_snippet_creation(self):
        """Test that a snippet is created correctly."""
        snippet = Snippet.objects.get(id=self.snippet.id)
        self.assertEqual(snippet.snippet_title, "Test Snippet")
        self.assertEqual(snippet.note, "This is a test note.")
        self.assertEqual(snippet.created_by, self.user)

    def test_snippet_tags(self):
        """Test that tags are correctly assigned to a snippet."""
        self.assertEqual(self.snippet.tags.count(), 2)
        self.assertIn(self.tag1, self.snippet.tags.all())
        self.assertIn(self.tag2, self.snippet.tags.all())

    def test_snippet_str_method(self):
        """Test the __str__ method of Snippet."""
        self.assertEqual(str(self.snippet), "Test Snippet")

    def test_filter_snippets_by_user(self):
        """Test that snippets can be filtered by created_by."""
        user_snippets = Snippet.objects.filter(created_by=self.user)
        self.assertEqual(user_snippets.count(), 1)
        self.assertEqual(user_snippets.first(), self.snippet)

    from django.utils.timezone import now, timedelta

    def test_snippet_ordering(self):
        """Test that snippets are ordered by newest first."""
        # Create an older snippet by setting an earlier timestamp
        older_snippet = Snippet.objects.create(
            snippet_title="Older Snippet",
            note="An older test note.",
            created_by=self.user
        )
        older_snippet.created_at = now() - timedelta(days=1)  # Set it to 1 day earlier
        older_snippet.save()  # Save the updated timestamp

        snippets = Snippet.objects.filter(created_by=self.user).order_by("-created_at")

        # Assert that the most recent snippet is first
        self.assertEqual(snippets.first(), self.snippet)
        self.assertEqual(snippets.last(), older_snippet)

class TagDetailAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a tag instance for testing
        self.tag = Tag.objects.create(tag_title='Test Tag')

        # Create a snippet associated with the tag
        self.snippet = Snippet.objects.create(
            snippet_title='Test Snippet',
            note='This is a test snippet',
            created_by=self.user
        )
        self.snippet.tags.add(self.tag)

        # URL for the TagDetailAPI view
        self.url = reverse('tag-detail', kwargs={'pk': self.tag.pk})

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tag_detail_authenticated(self):
        # Make a GET request to the TagDetailAPI view
        response = self.client.get(self.url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the correct tag title
        self.assertEqual(response.data['tag_title'], self.tag.tag_title)

        # Check that the response data includes snippets associated with the tag
        self.assertIn('snippets', response.data)
        self.assertEqual(len(response.data['snippets']), 1)
        self.assertEqual(response.data['snippets'][0]['snippet_title'], self.snippet.snippet_title)

    def test_retrieve_tag_detail_unauthenticated(self):
        # Log out the user
        self.client.logout()

        # Make a GET request to the TagDetailAPI view without authentication
        response = self.client.get(self.url)

        # Check that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_nonexistent_tag(self):
        # URL for a non-existent tag
        nonexistent_url = reverse('tag-detail', kwargs={'pk': 999})

        # Make a GET request to the TagDetailAPI view with a non-existent tag ID
        response = self.client.get(nonexistent_url)

        # Check that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)





