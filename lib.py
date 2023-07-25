from sys import path
path.append('\\Program Files\\Microsoft.NET\\ADOMD.NET\\160')

from pyadomd import Pyadomd
from pandas import DataFrame

conn_str = 'Provider=MSOLAP;Data Source=localhost;Catalog=AdventureWorks;'

def get_data(x):
  with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(x) as cur:
      df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
      # add fill na
  return df

query = """EVALUATE Product"""
get_data(query)




