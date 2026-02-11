
# NOTE nur für DEV Modus -- entfernen wegen DIP
from infrastructure.mongo.mongo_connection import MongoConnection
from infrastructure.mongo.mongo_repository import MongoRepository

from core.ports.base_repository_interface import BaseRepositoryInterface
from config.mongo_config import MongoCollection, MongoDatabase, MongoUser
from config.pipeline_config import COMPANY_PIPELINE, STAGED_FINANCEDATA_PIPELINE
import logging
logger = logging.getLogger(__name__)


def run_pipeline(repo : BaseRepositoryInterface, pipeline):
    repo.execute_pipeline(pipeline)


if __name__ == "__main__":
    with MongoConnection(MongoUser.APPUSER) as conn:
        #finance_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.FINANCEDATA)
        #company_repo = MongoRepository(conn, MongoDatabase.PROCESSED, MongoCollection.COMPANYDATA)
        raw_eod =  MongoRepository(conn, MongoDatabase.RAW, MongoCollection.EODPRICE)
        raw_profile_repo = MongoRepository(conn, MongoDatabase.RAW, MongoCollection.PROFILE)
        run_pipeline(raw_eod, STAGED_FINANCEDATA_PIPELINE)