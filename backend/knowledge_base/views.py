from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .models import Category, Document
from .serializers import CategorySerializer, DocumentSerializer

from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        # self.update_category_path(serializer.instance)

    def perform_update(self, serializer):
        serializer.save()
        # self.update_category_path(serializer.instance)

    def update_category_path(self, category):
        if category.parent:
            category.path = f"{category.parent.path}/{category.name}"
        else:
            category.path = category.name
        category.save()


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Document deleted successfully"}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_category_tree(request):
    categories = Category.objects.all()
    tree = build_category_tree(categories)
    return Response(tree)


def build_category_tree(categories):
    category_dict = {
        category.id: {
            "id": category.id,
            "name": category.name,
            "path": category.path,
            "children": [],
        }
        for category in categories
    }
    root_categories = []

    for category in categories:
        parent_id = category.parent_id
        if parent_id:
            parent = category_dict.get(parent_id)
            if parent:
                parent["children"].append(category_dict[category.id])
        else:
            root_categories.append(category_dict[category.id])

    return root_categories


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_category_documents(request, category_id):
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 20))

    documents = Document.objects.filter(category_id=category_id)
    total = documents.count()

    paginator = Paginator(documents, per_page)
    try:
        documents_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        documents_page = paginator.page(paginator.num_pages)

    serializer = DocumentSerializer(documents_page, many=True)

    return Response(
        {
            "total": total,
            "page": page,
            "per_page": per_page,
            "documents": serializer.data,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_documents(request):
    query = request.GET.get("query", "")
    category_id = request.GET.get("category", None)

    documents = Document.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )

    if category_id:
        documents = documents.filter(category_id=category_id)

    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)
