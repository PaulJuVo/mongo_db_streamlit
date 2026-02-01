#!/bin/bash
set -e

echo "Creating mongo users..."


MONGO_CMD="mongosh admin -u $MONGODB_INITDB_ROOT_USERNAME -p $MONGODB_INITDB_ROOT_PASSWORD --quiet"


$MONGO_CMD --eval "
  db = db.getSiblingDB('$MONGO_APPUSER_AUTH_DB');
  db.createUser({user: '$MONGO_APPUSER_USER', pwd: '$MONGO_APPUSER_PASSWORD', roles: [{role: 'readWrite', db: '$MONGO_APPUSER_AUTH_DB'}, {role: 'readWrite', db: '$MONGO_DASHBOARDUSER_AUTH_DB'}]});

  db = db.getSiblingDB('$MONGO_DASHBOARDUSER_AUTH_DB');
  db.createUser({user: '$MONGO_DASHBOARDUSER_USER', pwd: '$MONGO_DASHBOARDUSER_PASSWORD', roles: [{role: 'read', db: '$MONGO_DASHBOARDUSER_AUTH_DB'}]});
"

echo "All users created successfully."