from airflow import DAG
from airflow.utils.dates import days_ago
from meltano.providers.airflow import MeltanoOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="northwind_daily_pipeline",
    default_args=default_args,
    description="Pipeline diário de extração e carga de dados da northwind com Meltano",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    
    extract_postgres = MeltanoOperator(
        task_id="extract_postgres",
        meltano_command="run tap-postgres target-parquet-postgres",
        env={"EXECUTION_DATE": "{{ ds }}"},  
    )

    
    extract_csv = MeltanoOperator(
        task_id="extract_csv",
        meltano_command="run tap-csv target-parquet-csv",
        env={"EXECUTION_DATE": "{{ ds }}"},  
    )

    
    [extract_postgres >> extract_csv]
