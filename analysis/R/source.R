rm(list = ls())

source("R/config.R")
source("R/data.R")
source("R/gaechteretal.R", echo = TRUE)
source("R/viz.R")

# install.packages("DescTools")
# library(DescTools)
# create_article("../reports/researchProposal.Rmd")

rmarkdown::render(input = "../reports/Treatments.Rmd",
                  output_format = "all",
                  output_file = "Treatments")
