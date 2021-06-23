rm(list = ls())

# source("R/config.R")
# source("R/data.R")
# source("R/gaechteretal.R", echo = TRUE)
# source("R/viz.R")

library(rmarkdown)
library(distill)

# Render HTML Report -----
rmarkdown::render(input = "../reports/01_dataGMTV.Rmd",
                  output_format = "distill_article",
                  output_dir = "../reports/html/",
                  output_file = "01_GMTV")

rmarkdown::render(input = "../reports/02_dataProcessing.Rmd",
                  output_format = "distill_article",
                  output_dir = "../reports/html/",
                  output_file = "02_Replication")

rmarkdown::render(input = "../reports/03_dataAnalyses.Rmd",
                  output_format = "distill_article",
                  output_dir = "../reports/html/",
                  output_file = "03_Analyses")

# Render PDF Report -----
# rmarkdown::render(input = "../reports/01_dataGMTV.Rmd",
#                   output_format = "pdf_document",
#                   output_dir = "../reports/pdf/",
#                   output_file = "01_GMTV")
# 
# rmarkdown::render(input = "../reports/02_dataProcessing.Rmd",
#                   output_format = "pdf_document",
#                   output_dir = "../reports/pdf/",
#                   output_file = "02_Replication")

rmarkdown::render(input = "../reports/03_dataAnalyses.Rmd",
                  output_format = "pdf_document",
                  output_dir = "../reports/pdf/",
                  output_file = "03_Analyses")