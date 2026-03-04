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
                  {
                    "$lookup": {
                      "from": MongoCollection.COMPANYDATA.value,
                      "localField": "symbol",
                      "foreignField": "symbol",
                      "as": "companyData"
                    }
                  },
                  {
                    "$replaceRoot": {
                      "newRoot": {
                        "$mergeObjects": [
                          { "$arrayElemAt": [ "$companyData", 0 ] },
                          "$$ROOT"
                        ]
                      }
                    }
                  },
                  {
                    "$project": { "companyData": 0 }
                  },
                  {
                    "$group": {
                      "_id": {
                        "date": "$date",
                        "sector": "$sector"
                      },
                      "pcRatioMedian": {
                        "$median": {
                          "input": "$pcRatio",
                          "method": "approximate"
                        }
                      },
                      "peRatioMedian": {
                        "$median": {
                          "input": "$peRatio",
                          "method": "approximate"
                        }
                      },
                      "pfcfRatioMedian": {
                        "$median": {
                          "input": "$pfcfRatio",
                          "method": "approximate"
                        }
                      },
                      "psRatioMedian": {
                        "$median": {
                          "input": "$psRatio",
                          "method": "approximate"
                        }
                      }
                    }
                  },
                  {
                    "$project": {
                      "_id": 0,
                      "date": "$_id.date",      
                      "sector": "$_id.sector",  
                      "pcRatioMedian": 1,
                      "peRatioMedian": 1,
                      "pfcfRatioMedian": 1,
                      "psRatioMedian": 1
                    }
                  },
                  {
                    "$match": {
                        "sector": { "$exists": True }
                    }
                  },
                  {
                    "$out": {
                      "db": MongoDatabase.PROCESSED.value,
                      "coll": MongoCollection.SECTORDATA.value,
                      "timeseries": {
                        "timeField": "date",
                        "metaField": "sector",    
                        "granularity": "hours"      
                      }
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

