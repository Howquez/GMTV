# Themes -----
layout <- theme(panel.background = element_rect(fill = "white"),
                panel.grid = element_line(colour="gray", size=0),
                panel.grid.major.y = element_line(colour="gray", size=0.25),
                legend.key = element_rect(fill = "white"),
                axis.line.x.bottom = element_line(size = 0.25),
                axis.line.y.left = element_line(size = 0.25),
                plot.margin = unit(c(1,1,1,1), "cm"),
                legend.title = element_blank()
                )

# Static Graphs -----
# chose variable to plot
outcome <- "endowment"
for(outcome in outcomes){
  # line graph with 95%-CI -----
  plotDT <- summarySE(data = na.omit(longDT, cols = outcome), 
                      measurevar = outcome, 
                      groupvars=c("treatment", "round"),
                      na.rm = FALSE,
                      conf.interval = 0.95,
                      .drop = TRUE)
  
  temp <- plotDT[, outcome]

  # plot
  plot <- ggplot(data = plotDT, aes(x = round, y = temp, fill = treatment, color = treatment)) + # linetype = treatment
    layout +
    geom_errorbar(aes(ymin=temp-ci, ymax=temp+ci), width=.25, alpha = 0.5) +
    geom_line() +
    # geom_point() + 
    scale_x_continuous(name="Period",  breaks = 1:15) +
    scale_y_continuous(expand = c(0, 0), limits = c(0, NA)) +
    labs(y = outcome %>% str_to_title()) +
    scale_color_manual(values = wes_palette("Moonrise3", n = 2))

  plotTitle <- glue("plot{str_to_title(outcome)}")
  # assign(x = plotTitle,
  #        value = plot)
  ggsave(plot, file = glue("../figures/ggplot2/{plotTitle}.png"), 
         width = 14, 
         height = 10, 
         units = "cm",
         bg = "transparent")
  rm(list = c("plotTitle", "plot", "temp", "plotDT", "outcome"))
}

# HighcharteR -----
# see https://stackoverflow.com/questions/39752747/error-bars-with-highcharter
# plotDT <- summarySE(data = na.omit(longDT, cols = "endowment"), 
#                     measurevar = "endowment", 
#                     groupvars=c("treatment", "round"),
#                     na.rm = FALSE,
#                     conf.interval = 0.95,
#                     .drop = TRUE)
# 
# hchart(plotDT, "line", hcaes(x = round, y = endowment, group = treatment))
# highchart() %>%
#   hc_add_series(data=plotDT$endowment)
# 
# 
# library(dplyr)
# highchart() %>% 
#   hc_add_series(data = list_parse(mutate(plotDT, low = endowment - ci, high = endowment + ci)),
#                 type = "errorbar", color = "red", stemWidth = 5,  whiskerLength = 5) %>% 
#   hc_add_series(data = plotDT$endowment, color = "red")