from abc import ABC, abstractmethod
from typing import Any
import logging
from uuid import uuid4


class BaseETL(ABC):
    """Base framework for ETL operations."""

    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = logging.getLogger(self.__class__.__name__)
        self.source_name = self.__class__.__name__.replace("ETL", "").lower()

    @abstractmethod
    def extract(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def transform(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def load(self, data: list[dict[str, Any]]) -> dict[str, int]:
        pass

    def run(self, job_type: str = "full_sync") -> dict[str, Any]:
        self.logger.info("Starting %s for %s", job_type, self.source_name)
        job_id = self._create_sync_job(job_type)
        try:
            raw_data = self.extract()
            clean_data = self.transform(raw_data)
            result = self.load(clean_data)
            self._complete_sync_job(job_id, len(raw_data), result)
            return {
                "job_id": job_id,
                "status": "completed",
                "records_processed": len(raw_data),
                "records_added": result.get("added", 0),
                "records_updated": result.get("updated", 0),
                "records_errors": result.get("errors", 0),
            }
        except Exception as exc:
            self.logger.exception("ETL failed")
            self._fail_sync_job(job_id, str(exc))
            raise

    def _create_sync_job(self, job_type: str) -> str:
        job_id = str(uuid4())
        self.db.execute(
            """
            INSERT INTO data_sync_jobs (id, source, job_type, status, started_at)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (job_id, self.source_name, job_type, "running"),
        )
        self.db.commit()
        return job_id

    def _complete_sync_job(self, job_id: str, processed: int, result: dict[str, int]) -> None:
        self.db.execute(
            """
            UPDATE data_sync_jobs
            SET status = %s,
                records_processed = %s,
                records_added = %s,
                records_updated = %s,
                completed_at = NOW()
            WHERE id = %s
            """,
            (
                "completed",
                processed,
                result.get("added", 0),
                result.get("updated", 0),
                job_id,
            ),
        )
        self.db.commit()

    def _fail_sync_job(self, job_id: str, error_message: str) -> None:
        self.db.execute(
            """
            UPDATE data_sync_jobs
            SET status = %s,
                error_message = %s,
                completed_at = NOW()
            WHERE id = %s
            """,
            ("failed", error_message, job_id),
        )
        self.db.commit()
