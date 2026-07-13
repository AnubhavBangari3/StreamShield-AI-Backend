from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .retriever import retrieve_documents
from .serializers import KnowledgeSearchSerializer


@api_view(["POST"])
def knowledge_search(request):
    serializer = KnowledgeSearchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    query = serializer.validated_data["query"]
    k = serializer.validated_data["k"]

    docs = retrieve_documents(query, k)

    results = []

    for doc in docs:
        results.append(
            {
                "source": doc.metadata.get("source", "Unknown"),
                "content": doc.page_content,
            }
        )

    return Response(
        {
            "query": query,
            "matches": results,
        },
        status=status.HTTP_200_OK,
    )