
from core.ports.base_repository_interface import BaseRepositoryInterface
from config.mongo_config import STAGED_INCOMESTATEMENT_INDEX
from config.pipeline_config import COMPANY_PIPELINE, INCOME_STAGED, EOD_STAGED

class PipelineService:
    def __init__(self, 
                 eodprice_repo : BaseRepositoryInterface, 
                 income_repo : BaseRepositoryInterface,
                 staged_eodprice_repo : BaseRepositoryInterface, 
                 staged_income_repo : BaseRepositoryInterface,
                 profile_repo : BaseRepositoryInterface
                 ):
        self.eodprice_repo = eodprice_repo
        self.income_repo = income_repo
        self.staged_eodprice_repo = staged_eodprice_repo
        self.staged_income_repo = staged_income_repo
        self.profile_repo = profile_repo

    def run(self):
        self.profile_repo.execute_pipeline(COMPANY_PIPELINE)
        self.staged_eodprice_repo.drop()
        self.eodprice_repo.execute_pipeline(EOD_STAGED)
        self.staged_income_repo.drop()
        self.income_repo.execute_pipeline(INCOME_STAGED)
        self.staged_income_repo.run_db_command(STAGED_INCOMESTATEMENT_INDEX)

    def create_finance_data(self):
        '''
            loop all eod data in staging
                find last 4 eps in staged income
                calc pe ratio 
                write to processed.finance
        '''
        pass

