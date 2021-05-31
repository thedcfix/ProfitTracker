from azure.cosmos import exceptions, CosmosClient, PartitionKey
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

#queue
class Trend:

    def __init__(self):
        self.items = []
        self.name = ""
        
    def set_name(self, name):
        self.name = name

    def put(self, el):
        self.items.append(el)

    def get(self):
        return self.items
    
    def balance(self):
        return round(sum(self.items), 2)

    def show(self):
        print(self.items)

# Initialize the Cosmos client
endpoint = "YOUR_ENDPOINT"
key = 'YOUR_KEY'

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
database_name = "Trading"
container_name = "positions"

db = client.get_database_client(database_name)
positions_container = db.get_container_client(container_name)

data_container = db.get_container_client("data")

positions = list(positions_container.read_all_items())
tickers = []

for pos in positions:
    tickers.append(pos["name"])

#removing duplicates
positions = list(dict.fromkeys(tickers))
values = list(data_container.read_all_items())

trend = []

for pos in positions:

    current = Trend()
    current.set_name(pos)

    for val in values:
        if pos == val["name"]:
            current.put(val["daily_gain"])

    trend.append(current)

for el in trend:
    print(el.name)
    el.show()
    print(el.balance())

#to be changed
i = 8

fig, ax = plt.subplots()
fig.canvas.set_window_title("Trend")

data = pd.DataFrame(trend[i].get(), columns=["Values"])
data["Sign"] = data["Values"] < 0

data["Values"].plot(kind="bar", color=data.Sign.map({True: (1.0, 0, 0, 0.7), False: (0, 0.6, 0, 0.7)}), ax=ax)
ax.axhline(0, color="k")

handle = [Patch(facecolor="orange", label=trend[i].name)]
ax.legend(handles=handle, framealpha=0.5)

plt.show()

print(trend[i].get())

df = pd.DataFrame(trend[i].get())
df = df.applymap(str).replace(r'\.',',',regex=True)
df.to_csv("data1.csv", sep=';', index=False)