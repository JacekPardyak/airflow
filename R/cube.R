#' @import methods
#' @export
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