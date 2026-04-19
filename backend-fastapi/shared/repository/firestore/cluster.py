"""Firestore Cluster repository implementation."""

import logging
from datetime import datetime
from typing import Optional, List

from google.cloud import firestore as fs

from shared.dto import ClusterDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.cluster import IClusterRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[ClusterDTO]:
    if data is None:
        return None
    return ClusterDTO(
        id=data.get("id"),
        normalized_filters=data.get("normalized_filters", ""),
        buyer_count=data.get("buyer_count", 0),
        display_name=data.get("display_name"),
        description=data.get("description"),
        category_id=data.get("category_id"),
        subcategory_id=data.get("subcategory_id"),
        is_active=data.get("is_active", True),
        is_deleted=data.get("is_deleted", False),
        last_matched_at=data.get("last_matched_at"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        created_by=data.get("created_by"),
        updated_by=data.get("updated_by"),
        version=data.get("version", 1),
    )


class FsClusterRepository(FsBaseRepository, IClusterRepository):
    """Firestore implementation of cluster repository."""

    def __init__(self, client):
        super().__init__(client, col.CLUSTERS)

    def get_or_create(self, normalized_filters: str, user_id: int = None) -> ClusterDTO:
        """Get existing cluster or create a new one. Uses transaction for atomicity."""

        @fs.transactional
        def _txn(transaction):
            # Query for existing cluster
            query = self.collection.where(
                "normalized_filters", "==", normalized_filters
            ).where("is_deleted", "==", False)
            docs = list(query.stream())

            now = datetime.utcnow()

            if docs:
                doc = docs[0]
                data = doc.to_dict()
                updates = {
                    "buyer_count": (data.get("buyer_count") or 0) + 1,
                    "updated_at": now,
                    "updated_by": user_id,
                }
                transaction.update(doc.reference, updates)
                data.update(updates)
                return data

            # Create new - get next ID
            counter_ref = self.client.collection("_counters").document(self.collection_name)
            counter_snap = counter_ref.get(transaction=transaction)
            current = counter_snap.get("value") if counter_snap.exists else 0
            next_id = current + 1
            transaction.set(counter_ref, {"value": next_id})

            data = {
                "id": next_id,
                "normalized_filters": normalized_filters,
                "buyer_count": 1,
                "is_active": True,
                "is_deleted": False,
                "created_by": user_id,
                "updated_by": user_id,
                "created_at": now,
                "updated_at": now,
                "version": 1,
            }
            doc_ref = self.collection.document(str(next_id))
            transaction.set(doc_ref, data)
            return data

        transaction = self.client.transaction()
        result = _txn(transaction)
        return _to_dto(result)

    def get_by_normalized_filters(self, normalized_filters: str) -> Optional[ClusterDTO]:
        data = self._query_one(normalized_filters=normalized_filters, is_deleted=False)
        return _to_dto(data)

    def get_not_deleted(self, id: int) -> Optional[ClusterDTO]:
        data = self.get_by_id(id)
        if data and not data.get("is_deleted", False):
            return _to_dto(data)
        return None

    def get_active_clusters(self, skip: int = 0, limit: int = 100) -> List[ClusterDTO]:
        results = self._query_many(
            filters=[
                ("is_active", "==", True),
                ("is_deleted", "==", False),
            ],
            order_by="buyer_count",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def update_cluster(self, id: int, user_id: int = None, **kwargs) -> Optional[ClusterDTO]:
        data = self.get_by_id(id)
        if not data or data.get("is_deleted", False):
            return None

        kwargs["updated_by"] = user_id
        kwargs["updated_at"] = datetime.utcnow()
        kwargs["version"] = (data.get("version") or 0) + 1

        self.collection.document(str(id)).update(kwargs)
        data.update(kwargs)
        return _to_dto(data)

    def soft_delete_cluster(self, id: int, user_id: int = None) -> Optional[ClusterDTO]:
        data = self.get_by_id(id)
        if not data or data.get("is_deleted", False):
            return None

        updates = {
            "is_deleted": True,
            "updated_by": user_id,
            "updated_at": datetime.utcnow(),
        }
        self.collection.document(str(id)).update(updates)
        data.update(updates)
        return _to_dto(data)
