
usethis::use_git_config(user.name = "JacekPardyak", 
                        user.email = "jacek.pardyak@gmail.com")
usethis::create_github_token()
gitcreds::gitcreds_set()

library(devtools)
#create_package("~/package")
#use_git()
usethis::use_package("methods")
use_r("strsplit1")
#use_r("lib")
use_r("query")
#use_r("cube")
# remember this
#'
#' @param x A character vector with one element.
#' @param split What to split on.
#'
#' @return A character vector.
#' @export
#'
#' @examples
#' x <- "alfa,bravo,charlie,delta"
#' strsplit1(x, split = ",")
#'
load_all()
exists("strsplit1", where = globalenv(), inherits = FALSE)
check()
use_mit_license()

document()
install()

library(radomd)

x <- "alfa,bravo,charlie,delta"
strsplit1(x, split = ",")
