from rest_framework import serializers


class KnowledgeSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)
    k = serializers.IntegerField(
        required=False,
        default=3,
        min_value=1,
        max_value=10,
    )