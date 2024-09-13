from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SingleDocumentQASerializer
from .services import get_single_document_qa

# from .permissions import HasDocumentPermission


class SingleDocumentQAView(APIView):
    # permission_classes = [HasDocumentPermission]

    def post(self, request):
        serializer = SingleDocumentQASerializer(data=request.data)
        if serializer.is_valid():
            response = get_single_document_qa(
                document_id=serializer.validated_data["document_id"],
                messages=serializer.validated_data["messages"],
                stream=serializer.validated_data["stream"],
            )
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
