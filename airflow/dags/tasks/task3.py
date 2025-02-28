import pandas as pd
from pymongo import MongoClient
import sys
import os
from datetime import datetime

# Obtém a data do argumento ou usa a data atual
if len(sys.argv) > 1:
    date = sys.argv[1][:10]
else:
    date = datetime.today().strftime('%Y-%m-%d')

print(f"[INFO] Data utilizada: {date}")

# Caminhos dos arquivos CSV
base_path = "/workspaces/code-challenge/data/postgres"
csv_path = f"/workspaces/code-challenge/data/csv/{date}/data.csv"

files = {
    "orders": f"{base_path}/orders/{date}/data.csv",
    "products": f"{base_path}/products/{date}/data.csv",
    "customers": f"{base_path}/customers/{date}/data.csv",
    "order_details": csv_path
}

# Verifica se os arquivos existem antes de tentar carregá-los
for key, path in files.items():
    if not os.path.exists(path):
        print(f"[ERRO] Arquivo não encontrado: {path}")
        sys.exit(1)

# Carrega os dados
orders = pd.read_csv(files["orders"])[["order_id", "order_date", "customer_id"]].set_index("order_id")
products = pd.read_csv(files["products"])[["product_id", "product_name"]].set_index("product_id")
customers = pd.read_csv(files["customers"])[["customer_id", "company_name"]].set_index("customer_id")
order_details = pd.read_csv(files["order_details"])

# Junta os dados
orders = orders.join(customers, on="customer_id")
order_details = order_details.join(products, on="product_id")

# Transforma os dados
data = []
for order_id in order_details["order_id"].unique():
    json_order = order_details[order_details["order_id"] == order_id].drop("order_id", axis=1).to_dict("records")
    order = {
        "order_id": order_id,
        "order_date": orders.loc[order_id]["order_date"],
        "company_name": orders.loc[order_id]["company_name"],
        "products": json_order,
        "db_execution_date": date
    }
    data.append(order)

details = pd.DataFrame(data).to_dict("records")

# Conexão com MongoDB
try:
    client = MongoClient("mongodb://dharma:4815162342@mongo-container-od0g:27017/")
    db = client['orders']
    collection = db['details']
    collection.insert_many(details)
    print("[INFO] Dados inseridos com sucesso no MongoDB.")
except Exception as e:
    print(f"[ERRO] Falha ao conectar ao MongoDB: {e}")
    sys.exit(1)
