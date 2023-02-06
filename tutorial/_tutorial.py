from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

#from custom_operator.sftp_operator import MakeOperator

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

# ----------------------------------------------------------------
from airflow.models.baseoperator import BaseOperator
from airflow.providers.sftp.hooks.sftp import SFTPHook

SFTP_NO_SUCH_FILE = 200

class HelloDBOperator(BaseOperator):
    def __init__(self, name: str, mysql_conn_id: str, database: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.mysql_conn_id = mysql_conn_id
        self.database = database

    def execute(self, context):
        hook = MySqlHook(mysql_conn_id=self.mysql_conn_id, schema=self.database)
        sql = "select name from user"
        result = hook.get_first(sql)
        message = f"Hello {result['name']}"
        print(message)
        return message
      
class MakeOperator(BaseOperator):
    def __init__(self, path: str, ssh_conn_id, **kwargs) -> None:
        super().__init__(**kwargs)
        self.path = path
        self.ssh_conn_id = ssh_conn_id

    def execute(self, context) -> bool :
        f = open(self.path, "r")
        lines = f.read()
        lines = lines.upper()
        path_out = self.path.replace("in", "out" )
        f = open(path_out, "w")
        f.write(lines)
        f.close()
        print(lines)
        self.hook = SFTPHook(self.ssh_conn_id)
        self.log.info('Poking for %s', self.path)
        try:
            self.hook.get_mod_time(self.path)
        except OSError as e:
            if e.errno != SFTP_NO_SUCH_FILE:
                raise e
            return False
        self.hook.close_conn()
        return True

class ROperator(BaseOperator):
    def __init__(self, code: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.code = code

    def execute(self, context) -> bool :
        #f = open(self.path, "r")
        #lines = f.read()
        #lines = lines.upper()
        #path_out = self.path.replace("in", "out" )
        #f = open(path_out, "w")
        #f.write(lines)
        #f.close()
        print(self.code)
        import subprocess
        cmd = f"/usr/bin/Rscript --vanilla -e '{self.code}'"
        retcode = subprocess.call(cmd, shell=True)
        print(retcode)
        return True
		
# -------------------------------------------------

#  def poke(self, context: dict) -> bool:
#        self.hook = SFTPHook(self.sftp_conn_id)
#        self.log.info('Poking for %s', self.path)
#        
#        self.hook.close_conn()
#        return True

# report_path
# local file
# remote file

# -----------------------------------------------------------------

with DAG(
    "_r_operator",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id="getwd",
        depends_on_past=False,
        bash_command="""/bin/Rscript -e '
print(getwd());setwd("/home/jacek"); print(getwd())'
""",
    )
    
    def _py_code():
        import os
        path = os.getcwd()
        print(path)	
	
    install_py = PythonOperator(
        task_id='install_py', 
        python_callable=_py_code,
    )
	
    def _install_r():
        import os
        cmd = "R --version"
        cmd = """/bin/Rscript -e 'rmarkdown::render("/data/share/airflow/dags/project/Rmd/file.Rmd",params=list(master="yarn-client"),run_pandoc=F)' """
        #cmd = "sudo apt -y install r-base"
        
        returned_value = os.system(cmd)
        print(returned_value)

    install_r = PythonOperator(
        task_id='install_r', 
        python_callable=_install_r,
    )
    
    run_r = BashOperator(
    task_id='A_get_users',
    bash_command=f'Rscript -e "print(2+2)"',
    #bash_command=f'sudo apt-get install -y r-base',
    )

    rcode = '''ans = 3 + 4;setwd("/home/jacek");
fileConn<-file("output.txt")
writeLines(c("Hello","World"), fileConn)
close(fileConn)'''
    make_task = ROperator(task_id="make-task", code=rcode)
#    t1 >> [t2, t3] >> make_task 
    t1 >> install_r >> run_r >> install_py
