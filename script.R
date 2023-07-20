#library(arrow)
#df <- read_feather('data.feather')
library(reticulate)
py_install("plotnine", pip=TRUE)
py_install("shiny", pip=TRUE)
source_python('script.py')
df <- get_data(5)
print(df)

# ---- 
# prepare data
library(tidyverse)
tribble(
  ~x, ~y,  ~z,
  "a", 2,  3.6,
  "b", 1,  8.5
) %>% write_csv("data_1.csv")

tribble(
  ~x, ~y,  ~z, ~u,
  "a", 2,  3.6, "i",
  "b", 1,  8.5, "j",
  "c", 1,  8.5, "k"
) %>% write_csv("data_2.csv")
