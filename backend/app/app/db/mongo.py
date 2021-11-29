from mongoengine import connect, Document, BooleanField, ObjectIdField, StringField
import os
connect = connect(db=os.getenv("MONGO_DB_NAME"), host=os.getenv("MONGO_DB_SERVER"), port=int(os.getenv("MONGO_DB_PORT")), username=os.getenv("MONGO_DB_USER"), password=os.getenv("MONGO_DB_PASSWORD"))