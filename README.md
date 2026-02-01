## DB

TEST

### PYMONGO DOK

[Pymongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/databases-collections/#database)

### SETUP

Beim ersten hochfahren auth enablen [how to](https://www.mongodb.com/docs/manual/tutorial/enable-authentication/)

User erstellen:

```javascript
raw >
  db.createUser({
    user: "rawUser",
    pwd: "password", // or cleartext password
    roles: [{ role: "readWrite", db: "raw" }],
  });
{
  ok: 1;
}
processed >
  db.createUser({
    user: "processedUser",
    pwd: "password", // or cleartext password
    roles: [
      { role: "readWrite", db: "processed" },
      { role: "read", db: "raw" },
    ],
  });
{
  ok: 1;
}
processed >
  db.createUser({
    user: "reportUser",
    pwd: "password", // or cleartext password
    roles: [{ role: "read", db: "processed" }],
  });
```

### DB ROLLEN

MONGO_RAW_USER=rawUser
read and write auf raw

MONGO_PROCESSED_USER=processedUser
read auf raw
read and write auf processed

MONGO_REPORT_USER=reportUser
read auf processed
