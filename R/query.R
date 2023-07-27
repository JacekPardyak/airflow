#' @import methods
#' @export
Query <- setClass(
  # Set the name for the class
  "Query",
  
  # Define the slots
  slots = c(
    cube = "character",
    columns  = "character",
    rows = "character",
    slicers   = "character",
    mdx   = "character"
  ),
  
  # Set the default values for the slots. (optional)
  prototype=list(
    cube = "",
    columns   = "",
    rows = "",
    slicers = "",
    mdx = ""
  ),
  
  # Make a function that can test to see if the data is consistent.
  # This is not called if you have an initialize function defined!
  validity=function(object)
  {
    if(length(object@rows)>100.0) {
      return("The velocity level is out of bounds.")
    }
    return(TRUE)
  },
)
#' @export
setGeneric(name="cube",
           def=function(theObject,position)
           {
             standardGeneric("cube")
           }
)
#' @export
setMethod(f="cube",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@cube <- position
            validObject(theObject)
            return(theObject)
          }
)
#' @export
setGeneric(
  name = "columns",
  def = function(theObject, string)
  {
    standardGeneric("columns")
  }
)
#' @export
setMethod(
  f = "columns",
  signature = "Query",
  definition = function(theObject, string)
  {
    theObject@columns <- string
    validObject(theObject)
    return(theObject)
  }
)
#' @export
setGeneric(
  name = "rows",
  def = function(theObject, string)
  {
    standardGeneric("rows")
  }
)
#' @export
setMethod(
  f = "rows",
  signature = "Query",
  definition = function(theObject, string)
  {
    theObject@rows <- string
    validObject(theObject)
    return(theObject)
  }
)
#' @export
setGeneric(
  name = "slicers",
  def = function(theObject, string)
  {
    standardGeneric("slicers")
  }
)
#' @export
setMethod(
  f = "slicers",
  signature = "Query",
  definition = function(theObject, string)
  {
    theObject@slicers <- string
    validObject(theObject)
    return(theObject)
  }
)
#' @export
setGeneric(
  name = "mdx",
  def = function(theObject, string)
  {
    standardGeneric("mdx")
  }
)
#' @export
setMethod(
  f = "mdx",
  signature = "Query",
  definition = function(theObject, string)
  {
    theObject@mdx <- string
    validObject(theObject)
    return(theObject)
  }
)
#' @export
setGeneric(
  name = "explore",
  def = function(theObject)
  {
    standardGeneric("explore")
  }
)
#' @export
setMethod(
  f = "explore",
  signature = "Query",
  definition = function(theObject)
  {
    if (nchar(theObject@mdx) == 0) {
      fmt <- "SELECT {%s} ON COLUMNS, {%s} ON ROWS FROM %s WHERE %s"
      mdx <-
        sprintf(
          fmt,
          paste(theObject@columns, collapse = ", "),
          paste(theObject@rows, collapse = ", "),
          theObject@cube,
          paste(theObject@slicers, collapse = ", ")
        )
    }
    else {
      mdx = theObject@mdx
    }
    return(mdx)
  }
)

#' @export
setGeneric(
  name = "execute",
  def = function(theObject)
  {
    standardGeneric("execute")
  }
)
#' @export
setMethod(
  f = "execute",
  signature = "Query",
  definition = function(theObject)
  {
    'from sys import path
path.append("%s")
from pyadomd import Pyadomd
conn_str = "%s"
def get_state():
  with Pyadomd(conn_str) as conn:
    df = print(conn.state)
    return df' %>%
      sprintf(Sys.getenv("adomd_path"), Sys.getenv("conn_str")) %>%
      writeLines('state.py')
    
    'from sys import path
path.append("%s")
from pyadomd import Pyadomd
from pandas import DataFrame
conn_str = "%s"
def get_data(x):
  with Pyadomd(conn_str) as conn:
    with conn.cursor().execute(x) as cur:
      df = DataFrame(cur.fetchone(), columns=[i.name for i in cur.description])
      df = df.fillna("NA") # needed to smoothly convert to R tibble
  return df' %>% sprintf(Sys.getenv("adomd_path"), Sys.getenv("conn_str")) %>% writeLines('lib.py')
    
    if ( nchar(theObject@mdx) == 0 & nchar(theObject@cube) == 0) {
      reticulate::source_python('state.py')
      return(get_state())
    }
    else if (nchar(theObject@mdx) == 0) {
      fmt <- "SELECT {%s} ON COLUMNS, {%s} ON ROWS FROM %s WHERE %s"
      mdx <-
        sprintf(
          fmt,
          paste(theObject@columns, collapse = ", "),
          paste(theObject@rows, collapse = ", "),
          theObject@cube,
          paste(theObject@slicers, collapse = ", ")
        )
    }
    else {
      mdx = theObject@mdx
    }
    reticulate::source_python('lib.py')
    df <- get_data(mdx)
    #unlink('lib.py')
    return(df)
  }
)
