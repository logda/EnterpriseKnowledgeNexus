from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Document, UserPermission


class KnowledgeBaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.category = Category.objects.create(
            name="Test Category", path="/Test Category"
        )

    def test_create_document(self):
        url = reverse("document-list")
        data = {
            "title": "Test Document",
            "content": "This is a test document",
            "category": self.category.id,
            "created_by": self.user.id,  # 添加这一行
        }
        response = self.client.post(url, data, format="json")
        print(f"Create Document Response: {response.status_code}")
        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(Document.objects.get().title, "Test Document")

    def test_get_document(self):
        document = Document.objects.create(
            title="Test Document",
            content="This is a test document",
            category=self.category,
            created_by=self.user,
        )
        url = reverse("document-detail", kwargs={"pk": document.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Document")

    def test_update_document(self):
        document = Document.objects.create(
            title="Test Document",
            content="This is a test document",
            category=self.category,
            created_by=self.user,
        )
        url = reverse("document-detail", kwargs={"pk": document.id})
        data = {
            "title": "Updated Test Document",
            "content": "This is an updated test document",
            "category": self.category.id,
            "created_by": self.user.id,  # 添加这一行
        }
        response = self.client.put(url, data, format="json")
        print(f"Update Document Response: {response.status_code}")
        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Document.objects.get().title, "Updated Test Document")

    def test_delete_document(self):
        document = Document.objects.create(
            title="Test Document",
            content="This is a test document",
            category=self.category,
            created_by=self.user,
        )
        url = reverse("document-detail", kwargs={"pk": document.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Document.objects.count(), 0)

    def test_create_category(self):
        url = reverse("category-list")
        data = {
            "name": "New Category",
            "parent": None,
            "path": "/New Category",  # 添加 path 字段
        }
        response = self.client.post(url, data, format="json")
        print(f"Create Category Response: {response.status_code}")
        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Category.objects.count(), 2
        )  # Including the one created in setUp
        self.assertEqual(Category.objects.last().name, "New Category")

    def test_get_categories(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the one created in setUp

    def test_update_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        data = {
            "name": "Updated Category",
            "parent": None,
            "path": "/Updated Category",  # 添加 path 字段
        }
        response = self.client.put(url, data, format="json")
        print(f"Update Category Response: {response.status_code}")
        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Category.objects.get(id=self.category.id).name, "Updated Category"
        )

    def test_delete_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
