from airflow import DAG
from airflow.utils.dates import days_ago
from meltano.providers.airflow import MeltanoOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="load_parquet_to_postgres",
    default_args=default_args,
    description="Carregar dados dos arquivos Parquet no PostgreSQL destino",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    start_task = EmptyOperator(task_id="start")

    load_parquet_to_postgres = MeltanoOperator(
        task_id="parquet_to_postgres",
        meltano_command="run parquet_to_postgres",
        env={
            "EXECUTION_DATE": "{{ ds }}"  
        },
    )

    end_task = EmptyOperator(task_id="end")

    start_task >> load_parquet_to_postgres >> end_task
