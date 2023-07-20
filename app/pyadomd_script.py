from sys import path
path.append('\\Program Files\\Microsoft.NET\\ADOMD.NET\\160')

from pyadomd import Pyadomd

conn_str = 'Provider=MSOLAP;Data Source=localhost;Catalog=AdventureWorks;'
query = """EVALUATE Product"""

with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(query) as cur:
        print(cur.fetchall())

from pandas import DataFrame

with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(query) as cur:
        df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
