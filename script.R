source("lib.R")
library(tidyverse)

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
