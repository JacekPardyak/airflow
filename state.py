from sys import path
path.append("/Program Files/Microsoft.NET/ADOMD.NET/160")
from pyadomd import Pyadomd
conn_str = "Provider=MSOLAP.8;Integrated Security=SSPI;Persist Security Info=True;Initial Catalog=Finance Model;Data Source=gs-dk-dwh1.global.team.blue;MDX Compatibility=1;Safety Options=2;MDX Missing Member Mode=Error;Update Isolation Level=2"
def get_state():
  with Pyadomd(conn_str) as conn:
    df = print(conn.state)
    return df
