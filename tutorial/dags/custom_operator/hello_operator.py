from airflow.models.baseoperator import BaseOperator
from airflow.operators.bash import BashOperator

class HelloOperator(BaseOperator):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context):
        message = f"Hello {self.name}"
        print(message)
        return message

class MakeOperator(BaseOperator):
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context):
        f = open(self.name, "r")
        lines = f.read()
        lines = lines.upper()
        path = self.name.replace("in", "out" )
        f = open(path, "w")
        f.write(lines)
        f.close()
        print(lines)
        BashOperator(
          task_id="bash_push",
          bash_command = 'echo "::::TXT::::" && '
          'echo {{ lines }}" && '
          'echo "value_by_return"',
          )
        return lines

# -------------------------------------------------
