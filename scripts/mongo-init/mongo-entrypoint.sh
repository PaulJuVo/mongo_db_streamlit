#!/bin/bash
set -e

echo "Creating mongo users..."


MONGO_CMD="mongosh admin --host $MONGO_HOST -u $MONGODB_INITDB_ROOT_USERNAME -p $MONGODB_INITDB_ROOT_PASSWORD --quiet"


$MONGO_CMD --eval "
  db = db.getSiblingDB('$MONGO_DB_RAW');
  db.createUser({user: '$MONGO_RAW_USER', pwd: '$MONGO_RAW_PASSWORD', roles: [{role: 'readWrite', db: '$MONGO_DB_RAW'}]});
  
  db = db.getSiblingDB('$MONGO_DB_PROCESSED');
  db.createUser({user: '$MONGO_PROCESSED_USER', pwd: '$MONGO_PROCESSED_PASSWORD', roles: [{role: 'readWrite', db: '$MONGO_DB_PROCESSED'}, {role: 'read', db: '$MONGO_DB_RAW'}]});
  
  db = db.getSiblingDB('$MONGO_DB_REPORT');
  db.createUser({user: '$MONGO_REPORT_USER', pwd: '$MONGO_REPORT_PASSWORD', roles: [{role: 'read', db: '$MONGO_DB_REPORT'}]});
"

echo "All users created successfully."