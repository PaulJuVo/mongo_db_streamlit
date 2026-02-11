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
            "_id": 1,
            "symbol": 1,
            "companyName": 1,
            "industry": 1
        }
    },
    {  
        "$out": {
            "db": MongoDatabase.PROCESSED.value,
            "coll": MongoCollection.COMPANYDATA.value,
        }
    }
]

STAGED_FINANCEDATA_PIPELINE = [
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
        "$lookup": {
            "from" : MongoCollection.INCOMESTATEMENT.value,
            "localField" : "symbol",
            "foreignField": "symbol",
            "let" : { "eod_date" : "$date"},
            "pipeline": [
               {
                   "$match": { 
                       "$expr" : { 
                           "$gte" : ["$$eod_date", { "$toDate" :"$fillingDate"}] 
                       }
                   }
               },
               {
                   "$sort" :{
                       "fillingDate" : -1
                   }
               },
               {
                   "$limit" : 1
               }
            ],
            "as" : "incomeStatement"
            
        }
    },
    {
        "$unwind": {
            "path" : "$incomeStatement",
            "preserveNullAndEmptyArrays" : True
        }
    },
    {
        "$addFields": {
            "incomeStatementDate": { "$toDate" : "$incomeStatement.date"},
            "incomeStatementFillingDate": { "$toDate" : "$incomeStatement.fillingDate"},
            "eps" : "$incomeStatement.eps",
            "epsdiluted" : "$incomeStatement.epsdiluted"
        }
    },
    {
        "$project": {
            "_id": 0,
            "symbol": 1,
            "date": 1,
            "adjClose": 1,
            "incomeStatementDate": 1,
            "incomeStatementFillingDate": 1,
            "eps": 1,
            "epsdiluted": 1,
        }
    },
    {
        "$out": {
            "db": MongoDatabase.RAW.value,
            "coll": MongoCollection.STAGED_FINANCEDATA.value,
        }
    }
]
