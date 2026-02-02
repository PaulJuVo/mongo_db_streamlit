## DB

TEST

### PYMONGO DOK

[Pymongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/databases-collections/#database)

### SETUP

docker compose up -d
docker compose up --build wenn änderung

streamlit run app/streamlit_app.py

### DB ROLLEN

MONGO_RAW_USER=rawUser
read and write auf raw

MONGO_PROCESSED_USER=processedUser
read auf raw
read and write auf processed

MONGO_REPORT_USER=reportUser
read auf processed
