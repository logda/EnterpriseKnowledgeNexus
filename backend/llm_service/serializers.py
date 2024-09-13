from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=["user", "assistant"])
    content = serializers.CharField()


class SingleDocumentQASerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    messages = MessageSerializer(many=True)
    stream = serializers.BooleanField()
