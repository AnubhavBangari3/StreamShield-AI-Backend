from django.core.management.base import BaseCommand

from knowledge_base.vector_store import build_vector_store


class Command(BaseCommand):
    help = "Load runbooks, create embeddings, and build the FAISS vector store."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Loading runbooks..."))

        vector_store = build_vector_store()

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ FAISS index created successfully!\n"
                f"Indexed {vector_store.index.ntotal} chunks."
            )
        )