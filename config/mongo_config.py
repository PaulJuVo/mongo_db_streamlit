from infrastructure.mongo.mongo_user import Mongo_user
from infrastructure.mongo.repositories import (
    EodPrice_Repository,
    IncomeStatement_Repository,
    Profile_Repository,
    FinanceData_Repository,
    CompanyData_Repository,
)

USER_CONFIG = {
    Mongo_user.RAWUSER: {
        "user": "MONGO_RAW_USER",
        "password": "MONGO_RAW_PASSWORD",
        "db": "MONGO_DB_RAW",
    },
    Mongo_user.PROCESSEDUSER: {
        "user": "MONGO_PROCESSED_USER",
        "password": "MONGO_PROCESSED_PASSWORD",
        "db": "MONGO_DB_PROCESSED",
    },
    Mongo_user.REPORTUSER: {
        "user": "MONGO_REPORT_USER",
        "password": "MONGO_REPORT_PASSWORD",
        "db": "MONGO_DB_REPORT",
    },
}

REPO_MAP = {
    Mongo_user.RAWUSER: [
        ("eodPrice", EodPrice_Repository),
        ("incomeStatement", IncomeStatement_Repository),
        ("profile", Profile_Repository),
    ],
    Mongo_user.PROCESSEDUSER: [
        ("eodPrice", EodPrice_Repository),
        ("incomeStatement", IncomeStatement_Repository),
        ("profile", Profile_Repository),
        ("financeData", FinanceData_Repository),
        ("companyData", CompanyData_Repository),
    ],
    Mongo_user.REPORTUSER: [
        ("financeData", FinanceData_Repository),
        ("companyData", CompanyData_Repository),
    ],
}
