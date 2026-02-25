from config.mongo_config import MongoCollection, MongoDatabase
from config.processed_schema import COMPANY_VALIDATION_SCHEMA

COMPANY_PIPELINE = [
    {
        "$match":{
            "$jsonSchema": COMPANY_VALIDATION_SCHEMA
        }
    },
    {
        "$project": {
            "_id": 0,
            "symbol": 1,
            "companyName": 1,
            "sector": {
                "$cond": {
                  "if": { "$eq": [ "$sector", "" ] },
                  "then": "Unknown",
                  "else": "$sector"
                }
            }
        }
    },
    {
        "$merge": {
            "into" :{
                "db": MongoDatabase.PROCESSED.value,
                "coll": MongoCollection.COMPANYDATA.value,
            },
            "on": "symbol",
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }
]

EOD_STAGED = [
    {
        "$unwind": "$historical"
    },
    {
        "$addFields": {
            "date": { "$toDate" : "$historical.date"},
            "adjClose" : "$historical.adjClose"
            
        }
    },
    {
        "$project": {
            "_id": 0,
            "symbol": 1,
            "date": 1,
            "adjClose": 1
        }
    },
    {
        "$merge": {
            "into" :{
                "db": MongoDatabase.RAW.value,
                "coll": MongoCollection.STAGED_EODPRICE.value,
            },
            "on": ["date", "symbol" ],
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }
]

INCOME_STAGED = [
    {
        "$project": {
            "_id": 0,
            "symbol": 1,
            "date": { "$toDate" : "$date"},
            "fillingDate": { "$toDate" : "$fillingDate"},
            "eps": 1,
            "epsdiluted" : 1,
            "calendarYear" : { "$toInt" : "$calendarYear"},
            "period" : 1, 
            "revenue" : 1,
            "weightedAverageShsOutDil" : 1
        }
    },
    {
        "$merge": {
            "into" :{
                "db": MongoDatabase.RAW.value,
                "coll": MongoCollection.STAGED_INCOMESTATEMENT.value,
            },
            "on": ["date", "symbol" ],
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }
]

CASHFLOW_STAGED = [
    {
        "$project": {
            "_id": 0,
            "symbol": 1,
            "date": { "$toDate" : "$date"},
            "fillingDate": { "$toDate" : "$fillingDate"},
            "calendarYear" : { "$toInt" : "$calendarYear"},
            "period" : 1, 
            "freeCashFlow" : 1,
            "operatingCashFlow": 1
        }
    },
    {
        "$merge": {
            "into" :{
                "db": MongoDatabase.RAW.value,
                "coll": MongoCollection.STAGED_CASHFLOW.value,
            },
            "on": ["date", "symbol" ],
            "whenMatched": "replace",
            "whenNotMatched": "insert"
        }
    }
]

