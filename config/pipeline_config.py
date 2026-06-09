from config.mongo_config import MongoCollection, MongoDatabase
from config.processed_schema import COMPANY_VALIDATION_SCHEMA

CONSTITUES = [{"$set": 
                            {"date": 
                                {"$convert": 
                                    {"input": "$date",
                                    "to": "date",
                                    "onError": 0,
                                    "onNull": 0
                                    }
                                }
                            }
                        },
                        {
                          "$merge": {
                            "into": MongoCollection.CONSTITUENTS.value,   
                            "on": ["_id"],        
                            "whenMatched": "replace",   
                            "whenNotMatched": "insert"  
                          }
                        }
                        ]
CONSTITUENTS_WIKI = [{"$set": 
                            {"date": 
                                {"$convert": 
                                    {"input": "$date",
                                    "to": "date",
                                    "onError": 0,
                                    "onNull": 0
                                    }
                                }
                            }
                        },
                        {
                          "$merge": {
                            "into": MongoCollection.CONST_WIKI.value,   
                            "on": ["_id"],        
                            "whenMatched": "replace",   
                            "whenNotMatched": "insert"  
                          }
                        }
                        ]
CONSTITUENTS_WIKI_CHANGES = [{"$set": 
                            {"date": 
                                {"$convert": 
                                    {"input": "$date",
                                    "to": "date",
                                    "onError": 0,
                                    "onNull": 0
                                    }
                                }
                            }
                        },
                        {
                          "$merge": {
                            "into": MongoCollection.CONST_WIKI_CHANGES.value,   
                            "on": ["_id"],        
                            "whenMatched": "replace",   
                            "whenNotMatched": "insert"  
                          }
                        }
                        ]

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
            "image": 1,
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

SECTOR_DATA = [
    # Früh filtern – nur Felder die du brauchst weiterreichen
    {
        "$project": {
            "symbol": 1,
            "date": 1,
            "pcRatio": 1,
            "peRatio": 1,
            "pfcfRatio": 1,
            "psRatio": 1
        }
    },
    {
    "$lookup": {
        "from": MongoCollection.SCD_CONSTITUENTS.value,
        "let": {
            "sym": "$symbol",
            "dt": "$date"
        },
        "pipeline": [
            {
                "$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": ["$symbol", "$$sym"]},  # ← symbol statt companyName
                            {"$lte": ["$fromDate", "$$dt"]},
                            {"$gte": ["$toDate", "$$dt"]}
                        ]
                    }
                }
            },
            {"$limit": 1},
            {"$project": {"_id": 1}}
        ],
        "as": "constituent"
    }
    },
    {"$match": {"constituent": {"$ne": []}}},
    {"$project": {"constituent": 0, "companyName": 0, "symbol": 0}},
    {
        "$group": {
            "_id": {
                "date": "$date",
                "sector": "$sector"
            },
            "pcRatios":   {"$push": "$pcRatio"},
            "peRatios":   {"$push": "$peRatio"},
            "pfcfRatios": {"$push": "$pfcfRatio"},
            "psRatios":   {"$push": "$psRatio"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "date":       "$_id.date",
            "sector":     "$_id.sector",
            "pcRatios":   1,
            "peRatios":   1,
            "pfcfRatios": 1,
            "psRatios":   1
        }
    }
]


SPXEW = [
    {
    "$project": {
      "fields": { "$objectToArray": "$$ROOT" },
      "_id": 0
      }
    },
    {
    "$unwind": "$fields"
    },
    {
        "$match": {
            "fields.k": { "$ne": "_id" }
        }
    },
    {
    "$project": {
      "date": {"$toDate" : "$fields.k"},
      "adjClose": "$fields.v.Close",
      "symbol": "SPXEW"
      }
    }
]


SP500 = [
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
            "symbol": "GSPC",
            "date": 1,
            "adjClose": 1
        }
    },
    {
        "$unionWith": {
            "coll": MongoCollection.SPXEW.value,
            "pipeline": SPXEW
        }
    },
    {
      "$out": {
        "db": MongoDatabase.PROCESSED.value,
        "coll": MongoCollection.SP500.value,
        "timeseries": {
          "timeField": "date",
          "metaField": "symbol",
          "granularity": "hours"      
        }
      }
    }
]

