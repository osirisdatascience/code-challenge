from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.external_task import ExternalTaskSensor
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

    wait_for_step_1 = ExternalTaskSensor(
        task_id="wait_for_step_1",
        external_dag_id="northwind_daily_pipeline",
        external_task_ids=["extract_postgres", "extract_csv"],
        allowed_states=["success"],
        execution_delta=None,  
        mode="poke",  
        timeout=600,  
        poke_interval=30,  
    )

    start_task = EmptyOperator(task_id="start")

    load_parquet_to_postgres = MeltanoOperator(
        task_id="parquet_to_postgres",
        meltano_command="run parquet_to_postgres",
        env={
            "EXECUTION_DATE": "{{ execution_date.strftime('%d-%m-%Y') }}"  
        },    
        provide_context=True,   
        log_output=True,
    )

    end_task = EmptyOperator(task_id="end")

    wait_for_step_1 >> start_task >> load_parquet_to_postgres >> end_task
