# import modules
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# import custom modules
from include.transform import transform_data
from include.load import load_data
from include.extract import extract_data
from include.util import get_api_key, get_database_conn


# getting helper parameters
api_id = get_api_key()[0]
api_key  = get_api_key()[1]
engine = get_database_conn()


# default dag arguments
default_args = {
        'owner': 'chu_ngwoke',
        'start_date': datetime(year=2024, month=3, day=30),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': None,
        'retry_dely': None
}


with DAG(
    'KingsFX_ETL',
    default_args = default_args,
    description = 'ETL to get Exchange Rates', 
    schedule_interval = '0 0 * * *',
    catchup = False
) as dag:
    
    # start task
    start_task = DummyOperator(
        task_id = 'Start_Pipeline'
    )
    
    # extract task

    extract_task = PythonOperator(
        task_id = 'Extract_Response',
        python_callable = extract_data,
        op_kwargs = {'api_id': api_id, 'api_key': api_key}
    )

    # transform task
    transform_task = PythonOperator(
        task_id = 'Transform_response',
        python_callable = transform_data
    )

    # load task
    # load_task = PythonOperator(
    #     task_id = 'Load_to_postgres',
    #     python_callable = load_data,
    #     op_kwargs = {'engine': engine, 'table': 'rates'}
    # )

    with TaskGroup(group_id = 'Load_tasks') as load_data_tasks:
        stage_file_task = SnowflakeOperator(
                task_id='stage_data_to_snowflake',
                snowflake_conn_id='snowflake_conn',
                sql=f"""
                PUT file://./opt/airflow/raw/data.csv @~
                """,
                autocommit=True,
                )

        load_task = SnowflakeOperator(
                task_id='load_to_snowflake',
                snowflake_conn_id='snowflake_conn',
                sql=f"""
                COPY INTO rates
                FROM @~/data.csv
                FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1)
                """,
                autocommit=True,
                )

        stage_file_task >> load_task

    #End task
    end_task = DummyOperator(
        task_id = 'End_Pipeline'
    )

# set dependencies
start_task >> extract_task >> transform_task >> load_data_tasks >> end_task

