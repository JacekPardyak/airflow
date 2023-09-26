library(radomd)
library(tidyverse)

# set environmental variables
Sys.setenv(adomd_path = "/Program Files/Microsoft.NET/ADOMD.NET/160", 
           conn_str = "Provider=MSOLAP.8;Integrated Security=SSPI;Persist Security Info=True;Initial Catalog=Finance Model;Data Source={local};MDX Compatibility=1;Safety Options=2;MDX Missing Member Mode=Error;Update Isolation Level=2")

# check query to be send to SSAS
Query() %>% explore()

# check if the connection can be opened
Query() %>% execute()

# get data using MDX constructor
df <- Query() %>%
  cube("[model]") %>%
  columns(c("[Measures].[FS-72 MRR New customer count]")) %>%
  rows(c("[D_DATE_ACCRUED].[MONTH_NAME].&[January]",   
         "[D_DATE_ACCRUED].[MONTH_NAME].&[February]" )) %>%
  slicers(c("[D_ORGANIZATION].[Budget brand country].[Netherlands]")) 
df %>% explore()
df %>% execute()

# get data using MDX directly
df <- Query() %>%
  mdx("EVALUATE D_ORGANIZATION") 
df %>% explore()
df %>% execute()

