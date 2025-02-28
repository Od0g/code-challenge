import psycopg2
import pandas as pd
import os
import sys
from datetime import datetime

# Obtém a data do argumento ou usa a data atual
if len(sys.argv) > 1:
    date = sys.argv[1][:10]
else:
    date = datetime.today().strftime('%Y-%m-%d')

print(f"[INFO] Data utilizada: {date}")

# Configurações do banco de dados
host = "localhost"
database = "northwind"
user = "northwind_user"
password = "thewindisblowing"

try:
    db_conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    db_cursor = db_conn.cursor()
    print("[INFO] Conexão com o banco de dados estabelecida.")
except Exception as e:
    print(f"[ERRO] Falha ao conectar ao banco de dados: {e}")
    sys.exit(1)

def get_table_names(db_cursor):
    try:
        db_cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        table_names = [name[0] for name in db_cursor.fetchall()]
        print(f"[INFO] Tabelas encontradas: {table_names}")
        return table_names
    except Exception as e:
        print(f"[ERRO] Falha ao obter tabelas: {e}")
        return []

def csv_export(db_cursor, table_name, date):
    try:
        select = f"SELECT * FROM {table_name}"
        SQL_for_file_output = f"COPY ({select}) TO STDOUT WITH CSV HEADER"
        
        path_file = f"/workspaces/code-challenge/data/postgres/{table_name}/{date}/data.csv"
        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        
        with open(path_file, 'w') as f_output:
            db_cursor.copy_expert(SQL_for_file_output, f_output)
        print(f"[INFO] Exportação concluída para {path_file}")
    except Exception as e:
        print(f"[ERRO] Falha ao exportar tabela {table_name}: {e}")

# Executa exportação para todas as tabelas
for table_name in get_table_names(db_cursor):
    csv_export(db_cursor, table_name, date)

# Fecha a conexão com o banco de dados
db_cursor.close()
db_conn.close()
print("[INFO] Conexão com o banco de dados encerrada.")
