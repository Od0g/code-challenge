# Indicium Tech Code Challenge

Este repositório contém minha solução para o desafio proposto pela Indicium Tech, onde desenvolvi um pipeline de dados completo para extrair, transformar e carregar dados de diferentes fontes.

## Contexto

A Indicium Tech trabalha com projetos de pipeline de dados, extraindo informações de múltiplas fontes e carregando-as em diferentes destinos, como data warehouses ou APIs.

Meu desafio foi projetar, desenvolver, implantar e manter uma pipeline que extraia dados diariamente de duas fontes (um banco de dados PostgreSQL e um arquivo CSV), armazenando esses dados primeiro localmente e depois carregando-os em um banco PostgreSQL.

## Descrição do Desafio

Recebi duas fontes de dados:

- Um banco de dados PostgreSQL (Northwind, uma base educacional da Microsoft, com a diferença de que a tabela **order_detail** foi removida).
- Um arquivo CSV contendo os detalhes dos pedidos (substituindo a tabela **order_detail**).

Minha solução deveria:

- Extrair os dados diariamente das duas fontes.
- Armazenar os dados extraídos localmente em arquivos organizados por data.
- Carregar esses dados posteriormente para um banco PostgreSQL.
- Permitir a execução do pipeline para qualquer dia no passado.
- Garantir que a pipeline fosse idempotente.
- Exibir os pedidos e seus detalhes em uma consulta final.

## Ferramentas Utilizadas

Seguindo as recomendações da Indicium, utilizei:

- **Airflow** para orquestrar a execução das tarefas.
- **PostgreSQL** como banco de dados.
- **MongoDB** para armazenar logs.
- **Meltano** para extrair e carregar os dados.
- **Docker** para conteinerização do ambiente.

## Estrutura do Projeto

```
/code-challenge
│── airflow/
│   ├── dags/  # Scripts de DAGs do Airflow
│   ├── logs/  # Logs de execução do Airflow
│   ├── airflow.cfg  # Configuração do Airflow
│── data/  # Diretório onde os arquivos extraídos são armazenados
│── dbmongo/  # Dados do MongoDB
│── docker-compose.yml  # Configuração do ambiente
│── requirements.txt  # Dependências do Airflow
```

## Como Configurar e Executar o Projeto

### 1. Configuração do Ambiente

Primeiro, clone o repositório e acesse o diretório do projeto:

```bash
git clone https://github.com/Od0g/code-challenge.git
cd code-challenge
```

Crie os diretórios necessários para armazenar os dados extraídos:

```bash
mkdir -p data/postgres
data/csv
```

### 2. Subindo os Contêineres Docker

Utilizei o Docker para gerenciar as dependências. Para iniciar os serviços:

```bash
docker-compose up -d
```

Isso iniciará:

- **PostgreSQL** na porta 5432
- **MongoDB** na porta 27017
- **Airflow** na porta 8080

Acesse o Airflow via navegador em `http://localhost:8080`.

### 3. Configuração das Conexões no Airflow

No Airflow, configurei as conexões para acessar as fontes de dados:

1. **PostgreSQL**: Adicionei uma conexão em `Admin > Connections`, com:

   - Conn ID: `northwind_db`
   - Conn Type: `Postgres`
   - Host: `localhost`
   - Port: `5432`
   - Login: `northwind_user`
   - Password: `thewindisblowing`
   - Database: `northwind`

2. **MongoDB**: Configurado similarmente com host `mongo-container-od0g`.

### 4. Executando a Pipeline

Para rodar a pipeline, ativei a DAG no Airflow e a executei manualmente ou aguardei sua execução automática.

```bash
# Para executar manualmente no terminal:
airflow dags trigger data_pipeline
```

A DAG executa as seguintes tarefas:

1. **Extrai os dados** do PostgreSQL e do CSV.
2. **Salva localmente** em `/data/postgres/{tabela}/{data}/` e `/data/csv/{data}/`.
3. **Carrega os dados** no banco de destino.
4. **Executa uma query final** para exibir os pedidos e detalhes.

### 5. Verificando o Resultado

Para validar que tudo rodou corretamente, fiz a seguinte query no banco PostgreSQL final:

```sql
SELECT o.order_id, o.order_date, d.product_id, d.quantity
FROM orders o
JOIN order_details d ON o.order_id = d.order_id;
```

Se tudo ocorreu bem, um CSV com os resultados foi gerado.

## Erros e Soluções

### 1. `services.networks must be a mapping`

Corrigi a identação da seção `networks` no `docker-compose.yml`:

```yaml
networks:
  default:
    driver: bridge
```

### 2. `could not open directory 'dbdata/' Permission denied`

Esse erro ocorreu ao tentar versionar diretórios do Docker no Git. A solução foi ignorar os diretórios no `.gitignore`:

```bash
echo 'dbdata/' >> .gitignore
git rm -r --cached dbdata/
```

### 3. `It looks like you are trying to access MongoDB over HTTP on the native driver port`

Isso aconteceu porque tentei acessar o MongoDB sem um cliente adequado. Resolvi conectando corretamente via `mongo` CLI ou ferramentas como Robo 3T.

## Conclusão

Esse desafio foi uma grande oportunidade para consolidar conhecimentos em pipelines de dados, Airflow, e ferramentas ETL. A pipeline está configurada para rodar diariamente, garantindo que os dados sejam extraídos, armazenados e carregados corretamente.

Caso tenha dúvidas ou sugestões, fique à vontade para entrar em contato ou abrir uma issue no repositório!

Obrigado!
