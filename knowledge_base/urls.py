from django.urls import path

from .views import knowledge_search

urlpatterns = [
    path(
        "search/",
        knowledge_search,
        name="knowledge-search",
    ),
]