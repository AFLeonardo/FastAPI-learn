from pymongo import MongoClient

#Base de datos local
#db_client = MongoClient().local # Default connection to localhost:27017

#Base de datos en la nube

db_client = MongoClient(
    "mongodb+srv://admin:tilin22@curso-python.kxqo5gb.mongodb.net/?appName=Curso-Python").test