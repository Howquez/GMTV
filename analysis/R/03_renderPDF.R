# Render PDF Report -----
rmarkdown::render(input = "R/04_rmd/01_dataGMTV.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/pdf/",
                  output_file = "01_GMTV")

rmarkdown::render(input = "R/04_rmd/02_dataProcessing.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/pdf/",
                  output_file = "02_Replication")

rmarkdown::render(input = "R/04_rmd/03_dataAnalyses.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/pdf/",
                  output_file = "03_Analyses")

print("PDFs rendered. You can find them in analysis/reports/pdf/. The processed data is stored in data/processed/.")