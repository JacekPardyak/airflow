from sys import path
path.append("/Program Files/Microsoft.NET/ADOMD.NET/160")
from pyadomd import Pyadomd
from pandas import DataFrame
conn_str = "Provider=MSOLAP.8;Integrated Security=SSPI;Persist Security Info=True;Initial Catalog=Finance Model;Data Source=gs-dk-dwh1.global.team.blue;MDX Compatibility=1;Safety Options=2;MDX Missing Member Mode=Error;Update Isolation Level=2"
def get_data(x):
  with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(x) as cur:
      df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
      df = df.fillna("NA") # needed to smoothly convert to R tibble
  return df
