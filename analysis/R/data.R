# # read raw data
# Lo000 <- read.csv("../data/simulation/Lo000.csv", stringsAsFactors = FALSE) %>% data.table()
# Hi000 <- read.csv("../data/simulation/Hi000.csv", stringsAsFactors = FALSE) %>% data.table()
# Lo033 <- read.csv("../data/simulation/Lo033.csv", stringsAsFactors = FALSE) %>% data.table()
# Hi033 <- read.csv("../data/simulation/Hi033.csv", stringsAsFactors = FALSE) %>% data.table()
# 
# 
# # pretend we had a treatment
# Lo000[, session.code := "Lo000"]
# Hi000[, session.code := "Hi000"]
# Lo033[, session.code := "Lo033"]
# Hi033[, session.code := "Hi033"]
# 
# dt <- rbindlist(list(Lo000, Hi000, Lo033, Hi033),
#                 use.names = FALSE)

# or use the data gathered in a demo session
dt <- read.csv("../data/demoSessions/all_apps_wide-2021-03-25.csv", stringsAsFactors = FALSE) %>% data.table()
dt <- dt[, session.code := "demoSession"]

# control variables
cRegex <- "participant\\.code$|participant\\..time_started|session\\.code$|_index_in_pages|Intro\\.1\\.player\\.window.*|Intro\\.1\\.player\\.browser|participant\\.payoff$|^Outro"
controlVariables <- str_subset(string = names(dt),
                               pattern = cRegex)
ct <- dt[, ..controlVariables]


# main data frame
mRegex <- "participant\\.code$|participant\\.time_started|session\\.code$|dPGG\\.1\\.group\\.id_in_subsession|\\.1\\.player.belief|endowment|contribution|stock|gain$|bot_active|EWE|disaster|Comprehension"
mainVariables <- str_subset(string = names(dt),
                            pattern = mRegex)
mt <- dt[, ..mainVariables]

# select first round belief data -----
firstRound <- mt[,
                 .(belief = dPGG.1.player.belief,
                   othersContribution = dPGG.1.group.total_contribution - dPGG.1.player.contribution,
                   ownContribution = dPGG.1.player.contribution,
                   conformity = dPGG.1.player.contribution - dPGG.1.player.belief/3)]

# add share as contribution/endowment
for(round in 1:15){
  cont <- glue("dPGG.{round}.player.contribution")
  endo <- glue("dPGG.{round}.player.endowment")
  mt[, glue("dPGG.{round}.player.share") := mt[[cont]]/mt[[endo]] ]
}


# refactor groupID such that it also contains treatment-info
mt[,
   groupID := paste(session.code, dPGG.1.group.id_in_subsession, 
                    sep = "_")]

# rename clusters
names(mt)[names(mt) == "session.code"] <- "treatment"



# DT Magic: calculate averages by group -----
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
mt[,]

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
  setnames(DTs[[i]], old = "value", new = outcomes[i])
}


# create long dt with rounds as rows -----
longDT <- Reduce(function(...) merge(..., by=c(cluster, "round"), all = TRUE), DTs)


# flag observations where at least one participant did not understand the game
noComp <- mt[Outro.1.player.Comprehension == 0,
             groupID] %>% unique()
longDT[,
       noComprehension := 0]
longDT[groupID %in% noComp,
       noComprehension := 1]


# drop observations (i.e. groups in rounds) with dropouts (bot_active == 1) and
# where round > 10
longDT <- longDT[bot_active == 0 & round <= 10]


# save data -----
demoSession <- longDT
save(demoSession, file = "../data/processed/demoSession.rda")
# save(longDT, file = "../data/processed/simulations.rda")
# write.csv(longDT, file ="../data/processed/simulations.csv")


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

