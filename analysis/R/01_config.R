# Packages -----
# see https://rstudio.com/resources/webinars/managing-packages-for-open-source-data-science/
listOfPackages <- c("renv",          # package management
                    "rang",          # package management
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
                    "lmtest",
                    "DescTools",     # gini coefficient
                    "downloadthis"   # download button 4 HTML reports
                    )


newPackages <- listOfPackages[!(listOfPackages %in% installed.packages()[, "Package"])]

if(length(newPackages) > 0){
  install.packages(newPackages)
}

for(package in listOfPackages){
  require(package, character.only = TRUE)
}

# create snapshot -----
# graph <- rang::resolve(pkgs = listOfPackages,
#                        snapshot_date = '2023-06-14')
# export_rang(graph, 'requirements/pre-reg.R')
# save(graph, file = 'requirements/pre-reg.rda')

# read most recent data -----
cFiles <- file.info(list.files(path = "../data/replication",
                               recursive = TRUE,
                               full.names = TRUE,
                               pattern = "all_apps_wide.csv$"),
                    extra_cols = FALSE)
recentCSV <- cFiles[cFiles$mtime == max(cFiles$mtime), ] %>% row.names()
recentCSV <- "../data/replication/all_apps_wide-2021-07-03.csv"