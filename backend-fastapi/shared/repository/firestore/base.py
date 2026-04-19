"""Base Firestore repository with auto-increment ID support."""

import logging
from google.cloud import firestore as fs

logger = logging.getLogger(__name__)


class FsBaseRepository:
    """Generic Firestore CRUD operations with auto-increment integer IDs."""

    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name
        self.collection = client.collection(collection_name)

    def _next_id(self) -> int:
        """Atomically increment and return the next integer ID for this collection."""
        counter_ref = self.client.collection("_counters").document(self.collection_name)

        @fs.transactional
        def increment(transaction):
            snapshot = counter_ref.get(transaction=transaction)
            current = snapshot.get("value") if snapshot.exists else 0
            next_val = current + 1
            transaction.set(counter_ref, {"value": next_val})
            return next_val

        transaction = self.client.transaction()
        return increment(transaction)

    def create(self, **kwargs):
        """Create a document with auto-increment integer ID."""
        doc_id = self._next_id()
        kwargs["id"] = doc_id
        self.collection.document(str(doc_id)).set(kwargs)
        logger.debug(f"Created {self.collection_name} id={doc_id}")
        return kwargs

    def get_by_id(self, id: int):
        """Get document by integer ID."""
        doc = self.collection.document(str(id)).get()
        return doc.to_dict() if doc.exists else None

    def get_all(self, skip: int = 0, limit: int = 100):
        """Get all documents with pagination."""
        docs = self.collection.limit(skip + limit).stream()
        results = [doc.to_dict() for doc in docs]
        return results[skip:]

    def update(self, id: int, **kwargs):
        """Update document fields."""
        doc_ref = self.collection.document(str(id))
        doc = doc_ref.get()
        if not doc.exists:
            return None
        doc_ref.update(kwargs)
        updated = doc_ref.get()
        logger.debug(f"Updated {self.collection_name} id={id}")
        return updated.to_dict()

    def delete(self, id: int) -> bool:
        """Hard delete a document."""
        doc_ref = self.collection.document(str(id))
        doc = doc_ref.get()
        if not doc.exists:
            return False
        doc_ref.delete()
        logger.debug(f"Deleted {self.collection_name} id={id}")
        return True

    def soft_delete(self, id: int, user_id: int = None):
        """Mark document as deleted."""
        from datetime import datetime
        return self.update(id, is_deleted=True, updated_by=user_id, updated_at=datetime.utcnow())

    def _query_one(self, **filters):
        """Query for a single document matching all filters."""
        query = self.collection
        for field, value in filters.items():
            query = query.where(field, "==", value)
        docs = list(query.limit(1).stream())
        return docs[0].to_dict() if docs else None

    def _query_many(self, filters: list = None, order_by: str = None,
                    order_dir: str = "ASCENDING", skip: int = 0, limit: int = 100):
        """Query for multiple documents with filters and ordering."""
        query = self.collection
        if filters:
            for field, op, value in filters:
                query = query.where(field, op, value)
        if order_by:
            direction = fs.Query.ASCENDING if order_dir == "ASCENDING" else fs.Query.DESCENDING
            query = query.order_by(order_by, direction=direction)
        docs = list(query.limit(skip + limit).stream())
        results = [doc.to_dict() for doc in docs]
        return results[skip:]
