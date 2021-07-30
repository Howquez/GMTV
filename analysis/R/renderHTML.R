# Render HTML Report -----
# rmarkdown::render(input = "reports/rmd/01_dataGMTV.Rmd",
#                   output_dir = "reports/html/",
#                   output_file = "01_GMTV")

rmarkdown::render(input = "reports/rmd/02_dataProcessing.Rmd",
                  output_dir = "reports/html/",
                  output_file = "02_Replication")

rmarkdown::render(input = "reports/rmd/03_dataAnalyses.Rmd",
                  output_dir = "reports/html/",
                  output_file = "03_Analyses")

print("PDFs rendered. You can find them in analysis/reports/html/. The processed data is stored in data/processed/.")