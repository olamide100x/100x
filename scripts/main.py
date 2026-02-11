import logging
import sys
from datetime import datetime

from utils.db import get_db_connection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"etl_{datetime.now().strftime('%Y%m%d')}.log"),
    ],
)

logger = logging.getLogger(__name__)


def run_all_etls() -> None:
    logger.info("ETL scheduler scaffold initialized")
    db = get_db_connection()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT NOW()")
            logger.info("Database connection check succeeded at %s", cur.fetchone()[0])
    finally:
        db.close()


if __name__ == "__main__":
    run_all_etls()
