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
    rows = "ddd",
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

setGeneric(name="cube",
           def=function(theObject,position)
           {
             standardGeneric("cube")
           }
)

setMethod(f="cube",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@cube <- position
            validObject(theObject)
            return(theObject)
          }
)

setGeneric(name="columns",
           def=function(theObject,position)
           {
             standardGeneric("columns")
           }
)

setMethod(f="columns",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@columns <- position
            validObject(theObject)
            return(theObject)
          }
)    

setGeneric(name="rows",
           def=function(theObject,position)
           {
             standardGeneric("rows")
           }
)

setMethod(f="rows",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@rows <- position
            validObject(theObject)
            return(theObject)
          }
)    

setGeneric(name="slicers",
           def=function(theObject,position)
           {
             standardGeneric("slicers")
           }
)

setMethod(f="slicers",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@slicers <- position
            validObject(theObject)
            return(theObject)
          }
)    

setGeneric(name="mdx",
           def=function(theObject,position)
           {
             standardGeneric("mdx")
           }
)

setMethod(f="mdx",
          signature="Query",
          definition=function(theObject,position)
          {
            theObject@mdx <- position
            validObject(theObject)
            return(theObject)
          }
)  

setGeneric(name="show",
           def=function(theObject)
           {
             standardGeneric("show")
           }
)

setMethod(f="show",
          signature="Query",
          definition=function(theObject)
          {if(nchar(theObject@mdx) == 0){
            fmt <- "SELECT {%s} ON COLUMNS, {%s} ON ROWS FROM %s WHERE %s"
            mdx <- sprintf(fmt, paste(theObject@columns, collapse = ", "), paste(theObject@rows, collapse = ", "), theObject@cube, paste(theObject@slicers, collapse = ", "))
          }
            else {
            mdx = theObject@mdx  
            }
            return(mdx)
          }
) 


setGeneric(name="execute",
           def=function(theObject)
           {
             standardGeneric("execute")
           }
)

setMethod(f="execute",
          signature="Query",
          definition=function(theObject)
          {
            fmt <- "SELECT {%s} ON COLUMNS, {%s} ON ROWS FROM %s WHERE %s"
            mdx <- sprintf(fmt, paste(theObject@columns, collapse = ", "), paste(theObject@rows, collapse = ", "), theObject@cube, paste(theObject@slicers, collapse = ", "))
            reticulate::source_python('lib.py')
            df <- get_data(mdx)
            return(df)
          }
)
