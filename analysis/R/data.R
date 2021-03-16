# read raw data
sim1 <- read.csv("../data/simulation/jawroz7g.csv", stringsAsFactors = FALSE) %>% data.table()
sim2 <- read.csv("../data/simulation/etvc9q2x.csv", stringsAsFactors = FALSE) %>% data.table()


# pretend we had a treatment
sim1[, session.code := "control"]
sim2[, session.code := "treatment"]

dt <- rbindlist(list(sim1, sim2),
                use.names = FALSE)

# or use the data gathered in a demo session
# dt <- read.csv("../data/demoSessions/all_apps_wide-2021-03-09.csv", stringsAsFactors = FALSE) %>% data.table()
# dt <- dt[, session.code := "demoSession"]

# control variables
cRegex <- "participant\\.code$|participant\\..time_started|session\\.code$|_index_in_pages|Intro\\.1\\.player\\.window.*|Intro\\.1\\.player\\.browser|participant\\.payoff$|^Outro"
controlVariables <- str_subset(string = names(dt),
                               pattern = cRegex)
ct <- dt[, ..controlVariables]


# main data frame
mRegex <- "participant\\.code$|participant\\.time_started|session\\.code$|dPGG\\.1\\.group\\.id_in_subsession|\\.1\\.player.belief|endowment|contribution|stock|gain$|bot_active|EWE|disaster"
mainVariables <- str_subset(string = names(dt),
                            pattern = mRegex)
mt <- dt[, ..mainVariables]


# add share as contribution/endowment
for(round in 1:15){
  cont <- glue("dPGG.{round}.player.contribution")
  endo <- glue("dPGG.{round}.player.endowment")
  mt[, glue("dPGG.{round}.player.share") := mt[[cont]]/mt[[endo]] ]
}


# rename clusters
names(mt)[names(mt) == "dPGG.1.group.id_in_subsession"] <- "groupID"
names(mt)[names(mt) == "session.code"] <- "treatment"


# DT Magic: calculate averages by group 
cluster <- c("treatment", "groupID")
outcomes <- c("contribution", "endowment", "share", "stock", "gain", "bot_active", "disaster", "EWE")

DTs <- list()
for(outcome in outcomes){
  if(outcome == "bot_active" | outcome == "disaster" | outcome == "EWE"){
    var = names(mt) %>% str_subset(pattern = glue("group\\.{outcome}$"))
  } else {
    var = names(mt) %>% str_subset(pattern = glue("player\\.{outcome}$"))
  }


  # this is gold from https://stackoverflow.com/questions/16513827/summarizing-multiple-columns-with-data-table
  averages = mt[, 
                lapply(.SD, mean, na.rm=TRUE), 
                by = cluster, 
                .SDcols=var
                ]
  
  # this is gold from # https://cran.r-project.org/web/packages/data.table/vignettes/datatable-reshape.html
  meltedAverages <- melt(averages, id.vars = cluster, measure.vars = var)
  DTname <- glue("{str_to_title(outcome)}")
  # assign(DTname,
  #        meltedAverages)
  DTs[[DTname]] <- meltedAverages
  rm(list = c("DTname", "meltedAverages", "averages", "var", "outcome"))
}


# rename variables
for(i in 1:length(outcomes)){
  DTs[[i]] <- DTs[[i]][,
                       .(treatment = treatment,
                         groupID = groupID,
                         round = str_replace_all(string = variable,
                                                 pattern = "\\D", 
                                                 replacement="") %>% as.integer(),
                         value # to be renamed afterwards
                       )
  ]
  # rename "value" to outcome variable
  setnames(DTs[[i]], "value", outcomes[i])
}

# create long dt with rounds as rows
# lapply(DTs, function(i) setkey(i, round))
longDT <- Reduce(function(...) merge(..., by=c(cluster, "round"), all = TRUE), DTs)


# drop observations (i.e. groups in rounds) with dropouts (bot_active == 1)
longDT <- longDT[bot_active == 0]



# OLD -----
# 
# ?assign()
# vars <- names(mt) %>% str_subset(pattern = "player\\.contribution$|endowment$|gain$")
# averages <- mt[, 
#                lapply(.SD, mean, na.rm=TRUE), 
#                by=treatment, # groupID, 
#                .SDcols=vars
# ] 
# 
# variables <- c("endowment", "contribution", "stock")
# for(var in variables){
#   for(round in 1:10){
#     col <- glue("dPGG.{round}.player.{var}")
#     x <- mean(mt[[col]])
#     glue("{var}: {x}") %>% print()
#   }
# }
#   

