from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from hide import MONGODB_URL
client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))


try:
    client.admin.command('Ping')
    print('Connected successfully!')
except Exception as e:
    print('Here',e)