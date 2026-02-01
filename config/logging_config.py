import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import time 

def performance_log(logger : logging.Logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(logging.INFO,f"→ {func.__name__} gestartet")
            try:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                logger.log(logging.INFO,f"← {func.__name__} beendet, Time={start_time - end_time}")
                return result
            except Exception as e:
                logger.log(logging.ERROR,f"Fehler in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator



def setup_logging():
    # Mongo-Logger
    mongo_logger = logging.getLogger("mongo")
    mongo_logger.setLevel(logging.INFO)
    fh_mongo = RotatingFileHandler("logs/mongo.log", maxBytes=1_000_000, backupCount=3)
    fh_mongo.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    mongo_logger.addHandler(fh_mongo)
    mongo_logger.propagate = False

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", filename="logs/app.log")