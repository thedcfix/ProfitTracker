from yahoo_fin import stock_info as si
import numpy as np
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from datetime import datetime
import hashlib

# inserting data into the DB
def insert_in_db(id, name, specific_name, purchase_date, purchase_quantity, purchase_price, current_quantity, purchase_fee):
    
    data = {    'id' : id,
                'name' : name,
                'specific_name' : specific_name,
                'purchase_date' : purchase_date,
                'purchase_quantity' : purchase_quantity,
                'purchase_price' : purchase_price,
                'current_quantity' : current_quantity,
                'purchase_fee' : purchase_fee
           }

    container.upsert_item(data)
    return data

today = str(datetime.today().date())
portfolio = {}

# Initialize the Cosmos client
endpoint = "YOUR_ENDPOINT"
key = 'YOUR_KEY'

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
database_name = 'Trading'
container_name = 'positions'

db = client.get_database_client(database_name)
container = db.get_container_client(container_name)


name = "SWDA"
specific_name = "SWDA.MI"
purchase_date = str("2021-04-19")
purchase_quantity = 5
purchase_price = 337.45
current_quantity = 5
purchase_fee = 2.1

id = hashlib.sha512((purchase_date + specific_name).encode()).hexdigest()

info = insert_in_db(id, name, specific_name, purchase_date, purchase_quantity, purchase_price, current_quantity, purchase_fee)
print(info)