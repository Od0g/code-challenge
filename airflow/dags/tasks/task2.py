import shutil
import os
import sys
from datetime import datetime

# Obtém a data do argumento ou usa a data atual
if len(sys.argv) > 1:
    date = sys.argv[1][:10]
else:
    date = datetime.today().strftime('%Y-%m-%d')

print(f"[INFO] Data utilizada: {date}")

input_file = "/workspaces/code-challenge/data/order_details.csv"
output = f"/workspaces/code-challenge/data/csv/{date}/data.csv"

try:
    os.makedirs(os.path.dirname(output), exist_ok=True)
    shutil.copy(input_file, output)
    print(f"[INFO] Arquivo copiado para {output}")
except Exception as e:
    print(f"[ERRO] Falha ao copiar o arquivo: {e}")
    sys.exit(1)