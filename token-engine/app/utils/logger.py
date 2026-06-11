import logging
from app.config import LOG_LEVEL

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)