# Render PDF Report -----
# rmarkdown::render(input = "reports/rmd/01_dataGMTV.Rmd",
#                   output_format = "pdf_document",
#                   output_dir = "reports/pdf/",
#                   output_file = "01_GMTV")

rmarkdown::render(input = "reports/rmd/02_dataProcessing.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/pdf/",
                  output_file = "02_Replication")

rmarkdown::render(input = "reports/rmd/03_dataAnalyses.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/pdf/",
                  output_file = "03_Analyses")

rmarkdown::render(input = "reports/rmd/04_prettyAnalyses.Rmd",
                  output_format = "pdf_document",
                  output_dir = "reports/prettyReports/",
                  output_file = "04_Analyses")

print("PDFs rendered. You can find them in analysis/reports/pdf/. The processed data is stored in data/processed/.")