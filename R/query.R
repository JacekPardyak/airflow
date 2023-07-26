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
