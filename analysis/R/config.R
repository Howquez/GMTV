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
                    "lubridate",     # working with dates
                    "plotly",        # interactive visualizations
                    "wesanderson",   # color palette
                    "gridExtra",
                    "patchwork",
                    "highcharter",   # get nice interactive viz
                    "Rmisc",         # Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
                    "data.table",
                    "magrittr",      # get %>% and %<>% operators
                    "sjPlot",        # regression tables
                    "stargazer",     # regression tables
                    "plm",           # clustered standard errors
                    "lmtest"
                    )


newPackages <- listOfPackages[!(listOfPackages %in% installed.packages()[, "Package"])]

if(length(newPackages) > 0){
  install.packages(newPackages)
}

for(package in listOfPackages){
  require(package, character.only = TRUE)
}

# renv::snapshot()