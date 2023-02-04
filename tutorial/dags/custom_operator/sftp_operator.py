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
