source("lib.R")
library(tidyverse)
Sys.setenv(adomd_path = "\\Program Files\\Microsoft.NET\\ADOMD.NET\\160", 
           conn_str = 'Provider=MSOLAP;Data Source=localhost;Catalog=AdventureWorks;')
Sys.getenv("adomd_path")
Sys.getenv("conn_str")

qry <- Query() %>%
  cube("[Analysis Services Tutorial]") %>%
  columns(c("[Measures].[Internet Sales Count]", "[Measures].[Internet Sales-Sales Amount]")) %>%
  rows(c("[Product].[Product Line].[Product Line].MEMBERS")) %>%
  slicers(c("[Sales Territory].[Sales Territory Country].[Australia]"))
query <- "SELECT {[Measures].[Internet Sales Count], [Measures].[Internet Sales-Sales Amount]} ON COLUMNS, {[Product].[Product Line].[Product Line].MEMBERS} ON ROWS FROM [Analysis Services Tutorial] WHERE [Sales Territory].[Sales Territory Country].[Australia]"
show(qry) == query

execute(qry)

qry <- Query() %>%
  mdx("SELECT {[Measures].[Internet Sales Count Like], [Measures].[InternetSales-Sales Amount]} ON COLUMNS, {[Product].[Product Line].[Product Line].MEMBERS} ON ROWS FROM [Analysis Services Tutorial] WHERE [Sales Territory].[Sales Territory Country].[Australia]")
show(qry)
execute(qry)

'from sys import path
path.append("/Program Files/Microsoft.NET/ADOMD.NET/160")
from pyadomd import Pyadomd
from pandas import DataFrame
conn_str = "Provider=MSOLAP;Data Source=localhost;Catalog=AdventureWorks;"
def get_data(x):
  with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(x) as cur:
      df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
      # add fill na
  return df'  %>% writeLines('lib.py', useBytes = TRUE)

?writeLines
