original <- read_dta(file="../data/gaechteretal/GMTV-data.dta") %>% data.table()

# select no punish out of the first 10 sessions as subsequent sessions added further treatment variations
original <- original[punish == 0 & exp_num <=10]

# setnames(original,
#          old = c("treat", "per", "gr_id", "sumputin", "tokens", "putin", "gdp"),
#          new = c("treatment", "round", "groupID", "groupContribution", "endowment", "contribution", "groupEndowment"))

longGaechter <- original[,
                         .(treatment = treat,
                           groupID = gr_id,
                           round = per,
                           contribution = sumputin/4,
                           endowment = gdp/4,
                           share = mean, # or sumputin/gdp
                           stock = gdp - sumputin + sumputin * 1.5)] %>% unique()

unique(original$gr_id) %>% length()

original[,
   .N,
   by = gr_id]

x <- original[gr_id == 501]
x[,
  debug := shift(gdp, n = -1, fill = NA, type = "lag")]
x[,
  gain := debug-gdp]
x[,
  efficiency := gain/sum]

original <- original[order(gr_id, per)]
x <- x[order(gr_id, per)]
View(x)
