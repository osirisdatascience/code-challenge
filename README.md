# Indicium Tech Code Challenge

## **Descrição do Projeto**
Este projeto é um desafio técnico desenvolvido para demonstrar a capacidade de planejar, implementar e manter uma pipeline de dados que extrai informações de múltiplas fontes, armazena os dados localmente e os carrega em um banco de dados de destino.

### **Arquitetura Geral**
A solução consiste em duas etapas principais:
1. **Extração e Armazenamento Local**:
   - Extrair dados de:
     - Banco de dados PostgreSQL (Northwind).
     - Arquivo CSV representando a tabela `order_details`.
   - Armazenar os dados extraídos como arquivos Parquet organizados por tabelas e por data de execução.

2. **Carregamento no Banco de Destino**:
   - Carregar os arquivos Parquet gerados no banco de dados PostgreSQL de destino, no schema `processed`.
   - Garantir que as tabelas `orders` e `order_details` estejam disponíveis para consultas.

---

## **Ferramentas Utilizadas**
- **Airflow**: Gerenciamento e agendamento de tarefas.
- **Meltano**: Pipeline ETL para extração e carregamento de dados.
- **PostgreSQL**: Banco de dados de origem e destino.
- **Docker Compose**: Orquestração dos serviços.

---

## **Estrutura do Projeto**

```plaintext
├── data
│   │── db_destination_persisted (persistir os dados quando populados no passo 2)
│   ├── processed
│   │   ├── postgres
│   │   │   └── orders (criada dinamicamente na primeira execução)
│   │   │       └── 2024-01-01 (criada dinamicamente)
│   │   │           └── orders.parquet
│   │   └── csv
│   │       └── 2024-01-01 (criada dinamicamente)
│   │           └── order_details.parquet
│   └── source
│       └── northwind.sql
│       └── order_details.csv
├── meltano_project
│   ├── meltano.yml
├── airflow
│   ├── dags
│   │   ├── postgres_csv_to_local_pipeline.py
│   │   ├── local_to_postgres_pipeline.py
│   └── logs
│   └── plugins
├── docker-compose.yml
└── requirements.txt
└── README.md

```

---

## **Configuração do Ambiente**

### **1. Pré-requisitos**
- Docker e Docker Compose instalados.
- Python 3.8+ instalado (se necessário rodar localmente).

### **2. Instalando Dependências**
Certifique-se de instalar as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### **3. Configuração do Docker Compose**
Suba os serviços:
```bash
docker-compose up -d
```
Isso iniciará:
- PostgreSQL.
- Airflow.
- Meltano.

---

## **Execução do Pipeline**

### **1. Extração e Armazenamento Local**
A DAG `extract_to_parquet` executa a extração dos dados de:
- Tabelas do banco `northwind`.
- Arquivo CSV de `order_details`.

Os dados extraídos serão armazenados em:
```plaintext
/data/processed/{source}/{table}/{execution_date}/{table}.parquet
```
Para rodar manualmente:
```bash
airflow dags trigger extract_to_parquet
```

### **2. Carregamento no Banco de Destino**
A DAG `load_parquet_to_postgres` carrega os arquivos Parquet no banco de destino (`destination`), no schema `processed`.

Para rodar manualmente:
```bash
airflow dags trigger load_parquet_to_postgres
```

### **3. Consulta de Resultado**
Após executar o pipeline, você pode consultar os dados no banco de destino:
```sql
SELECT o.order_id, o.customer_id, d.product_id, d.unit_price, d.quantity, d.discount
FROM processed.orders o
JOIN processed.order_details d ON o.order_id = d.order_id;
```

---

## **Customizações**
- **Data Retroativa**:
  - No Airflow, configure a data de execução para reprocessar os dados de uma data que desejar.

---

## **Requisitos Atendidos**
1. **Uso das ferramentas especificadas**: Airflow, Meltano, PostgreSQL.
2. **Idempotência**: Arquivos e carregamentos são organizados por data, evitando duplicação.
3. **Dependências explícitas**: Step 2 depende do sucesso do Step 1.
4. **Extração completa**: Todas as tabelas do PostgreSQL e o arquivo CSV são extraídos.
5. **Monitoramento e Logs**: Airflow fornece logs e visualização detalhada do pipeline.
6. **Reprocessamento por data**: Suporta execução diária e retroativa.
7. **Instruções claras**: Este README explica como executar e monitorar o pipeline.



