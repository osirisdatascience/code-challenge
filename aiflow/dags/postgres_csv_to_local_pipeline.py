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
    dag_id="northwind_daily_pipeline",
    default_args=default_args,
    description="Pipeline diário de extração e carga de dados da northwind com Meltano",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    start_task = EmptyOperator(task_id="start")
    
    extract_postgres = MeltanoOperator(
        task_id="extract_postgres",
        meltano_command="run postgres_to_parquet",
        env={"EXECUTION_DATE": "{{ execution_date.strftime('%d-%m-%Y') }}"},  
        provide_context=True,
        log_output=True,
    )
    
    extract_csv = MeltanoOperator(
        task_id="extract_csv",
        meltano_command="run csv_to_parquet",
        env={"EXECUTION_DATE": "{{ execution_date.strftime('%d-%m-%Y') }}"},  
        provide_context=True,  
        log_output=True,
    )

    end_task = EmptyOperator(task_id="end")
    
    start_task >> [extract_postgres >> extract_csv] >> end_task
