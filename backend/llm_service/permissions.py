from rest_framework.permissions import BasePermission
from knowledge_base.models import UserPermission, Document


class HasDocumentPermission(BasePermission):
    def has_permission(self, request, view):
        document_id = request.data.get("document_id")
        if not document_id:
            return False

        user = request.user
        try:
            document = Document.objects.get(id=document_id)
            return (
                UserPermission.objects.filter(
                    user=user,
                    category=document.category,
                    permission_type__in=["view", "edit"],
                ).exists()
                or user.is_staff
            )
        except Document.DoesNotExist:
            return False
