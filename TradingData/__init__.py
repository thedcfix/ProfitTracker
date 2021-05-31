import datetime
import logging

import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import yfinance as yf
from yahoo_fin import stock_info as si
import hashlib

# inserting data into the DB
def insert_in_db(id, date, name, value, delta, profit, container):

    data = {    'id' : id,
                'date' : date,
                'name' : name,
                'value' : value,
                'daily_gain' : delta,
                'daily_profit' : profit
           }
    
    container.upsert_item(data)

def read_items(container):

    item_list = list(container.read_all_items())

    return item_list

def main(req: func.HttpRequest) -> func.HttpResponse:

    today = str(datetime.datetime.today().date())
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
    data_container = db.get_container_client('data')

    items = read_items(container)

    for item in items:

        name = item.get('name')
        specific_name = item.get('specific_name')
        purchase_date = item.get('purchase_date')
        purchase_quantity = item.get('purchase_quantity')

        ticker = yf.Ticker(specific_name)
        value = float(si.get_live_price(specific_name))
        previous_close = ticker.info["previousClose"]

        delta = value - previous_close
        profit = delta * purchase_quantity

        delta = round(delta, 2)
        profit = round(profit, 2)
        value = round(value, 2)

        if(purchase_date != today):

            try:
                partial_profit = portfolio[name]
                portfolio[name] = partial_profit + profit
            except:
                portfolio[name] = profit

            id = hashlib.sha512((today + specific_name).encode()).hexdigest()
            profit = portfolio[name]
            insert_in_db(id, today, name, value, delta, profit, data_container)
        else:

            try:
                partial_profit = portfolio[name]
                portfolio[name] = round(partial_profit + (value - purchase_price) * purchase_quantity, 2)
            except:
                portfolio[name] = round((value - purchase_price) * purchase_quantity, 2)
                
            profit = portfolio[name]
            insert_in_db(id, today, name, value, delta, profit, data_container)


    return func.HttpResponse(f"200 success")