from django.urls import path
from .views import SingleDocumentQAView

urlpatterns = [
    path("qa/single/", SingleDocumentQAView.as_view(), name="single_document_qa"),
]
