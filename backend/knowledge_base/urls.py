from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    DocumentViewSet,
    get_category_tree,
    get_category_documents,
)


router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"documents", DocumentViewSet, basename="document")

urlpatterns = [
    path("", include(router.urls)),
    path("category/tree/", get_category_tree, name="category-tree"),
    path(
        "categories/<int:category_id>/documents/",
        get_category_documents,
        name="category-documents",
    ),
]
