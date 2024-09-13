from rest_framework import serializers
from .models import Category, Document


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "path"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "content",
            "category",
            "created_by",
            "created_at",
            "updated_at",
        ]
