from config.mongo_config import MongoCollection

PROFIL_SCHEMA = {
    "type": "object",
    "required": ["symbol", "industry"],
    "properties": {
        "symbol": {"type": "string"},
        "companyName": {"type": "string"},
        "industry": {"type": "string"},
    }
}
COMPANY_VALIDATION_SCHEMA = {
    "bsonType": "object",
    "required": [ "symbol", "industry"],
    "properties": {
        "symbol": { "bsonType": "string" },
        "industry":  { "bsonType": "string" },
        "companyName": { "bsonType": "string" }
    }
}
EODPRICE_SCHEMA = {
    "type": "object",
    "required": ["symbol"],
    "properties": {
        "symbol": {"type": "string"}
    }
}
INCOMESTATEMENT_SCHEMA = {
    "type": "object",
    "required": ["symbol", "date", "epsdiluted", "fillingDate", "period"],
    "properties": {
        "symbol": {"type": "string"},
        "epsdiluted": {"type": "number"},
        "date": {"type": "string"},
        "fillingDate": {"type": "string"},
        "period": {"type": "string"}
    }
}

VALIDATION_SCHEMAS = {
    MongoCollection.PROFILE.value: PROFIL_SCHEMA,
    MongoCollection.COMPANYDATA.value: COMPANY_VALIDATION_SCHEMA,
    MongoCollection.EODPRICE.value: EODPRICE_SCHEMA,
    MongoCollection.INCOMESTATEMENT.value : INCOMESTATEMENT_SCHEMA
}
