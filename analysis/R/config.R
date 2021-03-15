# Packages -----
# see https://rstudio.com/resources/webinars/managing-packages-for-open-source-data-science/
listOfPackages <- c("renv",          # package management
                    "rmarkdown",
                    "knitr",
                    "distill",       # good looking HTML articles
                    "kableExtra",    # HTML tables
                    "tidyverse",     # many useful packages
                    "haven",         # read dta data from stata
                    "glue",          # get some python-like string operations
                    # "stringr",       # working with strings included in tidyverse
                    "lubridate",     # working with dates
                    "plotly",        # interactive visualizations
                    "wesanderson",   # color palette
                    "highcharter",   # get nice viz
                    "Rmisc",         # Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
                    "data.table",
                    "magrittr"       # get %>% and %<>% opeartors
                    )

newPackages <- listOfPackages[!(listOfPackages %in% installed.packages()[, "Package"])]

if(length(newPackages) > 0){
  install.packages(newPackages)
}

for(package in listOfPackages){
  require(package, character.only = TRUE)
}

snapshot()
# create_article("../reports/replication.Rmd")
