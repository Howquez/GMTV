rm(list = ls())

source("R/01_config.R")
source("R/02_renderHTML.R")
source("R/03_renderPDF.R")

for(i in pacman::p_loaded()){print(paste0(i, ' (', pacman::p_ver(i), ')'))}
