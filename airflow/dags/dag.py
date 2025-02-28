from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
import pendulum

default_args = {
    'owner': '0d0g',
    'depends_on_past': False,
    'start_date': pendulum.today('UTC').add(days=-1),
    'retries': 1,
}

with DAG(
    'DAG-indicium',
    schedule=timedelta(days=1),
    default_args=default_args,
) as dag:
    t1 = BashOperator(
        task_id='task1',
        bash_command=f"""
            cd {dag.folder}/tasks/
            python3 task1.py {{{{ execution_date }}}}
        """,
    )

    t2 = BashOperator(
        task_id='task2',
        bash_command=f"""
            cd {dag.folder}/tasks/
            python3 task2.py {{{{ execution_date }}}}
        """,
    )

    t3 = BashOperator(
        task_id='task3',
        bash_command=f"""
            cd {dag.folder}/tasks/
            python3 task3.py {{{{ execution_date }}}}
        """,
    )

    [t1, t2] >> t3
