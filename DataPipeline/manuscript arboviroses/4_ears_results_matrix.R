

# Short description -------------------------------------------------------


#This routine was adapted from:
#Nekorchuk, D. M., et al (2021). Comparing malaria early detection methods in a 
#declining transmission setting in northwestern Ethiopia. BMC public health, 
#21(1), 788.



# Packages- -----------------------------------------------------------------


pacman::p_load(tidyverse, surveillance, lubridate, janitor, forcats, arrow)


# Import functions --------------------------------------------------------


source("functions_paper.R")


# Import main matrix ------------------------------------------------------


setwd("path")
result_main <- arrow::read_parquet("3_.parquet")


# Set data ---------------------------------------------------------------


ears_data <- result_main %>% 
  select(co_ibge,
         atend_arbov,
         week,
         populacao_2022,
         alarmC1_8w001)

ears_data <- ears_data %>% 
  rename(date = week,
         observed = atend_arbov,
         population = populacao_2022,
         alarm = alarmC1_8w001) %>% 
  mutate(alarm = as.logical(alarm),
         co_ibge = as.character(co_ibge))

srag_data <- result_main %>% 
  select(co_ibge,
         week,
         indic003) %>% 
  rename(date = week, 
         state_srag = indic003) %>% 
  mutate(state_srag = state_srag==1)


compare_ears <- function(ears_data,
                         srag_data,
                         week2,
                         week1_aps,
                         regiao, 
                         pre_week_search) {
  evi_data <- ears_data %>%
    filter(co_ibge == regiao) %>%
    filter(
      date > week1_aps,
      date < week2
    )
  
  srag_base <- srag_data %>%
    filter(co_ibge == regiao)
  
  evi_data <- evi_data %>%
    left_join(srag_base,
              by = c("date"="date")
    )
  sts_aps <- sts(
    observed = evi_data$observed,
    start = c(
      min(lubridate::epiweek(evi_data$date)),
      lubridate::epiweek(min(evi_data$date))
    ),
    frequency = 52,
    epoch = evi_data$date,
    epochAsDate = T,
    population = as.matrix(evi_data$population), # prevent error
    state = evi_data$state_srag,
    alarm = evi_data$alarm
  )
  this_ears_overlaps <- calculate_overlaps(
    list(as.data.frame(sts_aps)),
    pre_week_search
  )
  this_ears_res <- bind_cols(
    events_caught(this_ears_overlaps[[1]]),
    events_timely(this_ears_overlaps[[1]]),
    alarms_events(this_ears_overlaps[[2]])
  )
  return(list(
    aps = sts_aps,
    bmc_stat = this_ears_res,
    diff_alarms = this_ears_overlaps[[1]][[1]],
    diff_events = this_ears_overlaps[[2]][[1]],
    aa = this_ears_overlaps
  ))
}


# Run  --------------------------------------------------------------------


ime_not_ears_caught <- NULL
ime_not_ears_diff <- NULL
ime_not_ears_alarms <- NULL

cidades <- unique(result_main$co_ibge)

for (i in 1:length(cidades)) {
  
  j <- cidades[i]
  print(j)
  temp <- compare_ears(ears_data, 
                       srag_data,
                       regiao = j,
                       week1_aps = "2022-12-10",
                       week2 = "2024-02-26",
                       pre_week_search = 4
  )
  temp2 <- temp$bmc_stat %>% mutate(cod = j)
  temp4 <- temp$diff_alarms %>% mutate(cod = j)
  temp5 <- temp$diff_events %>% mutate(cod = j)
  ime_not_ears_caught <- rbind(ime_not_ears_caught, temp2)
  ime_not_ears_diff <- rbind(ime_not_ears_diff, temp4)
  ime_not_ears_alarms<- rbind(ime_not_ears_alarms, temp5)
}


# Export results ----------------------------------------------------------


setwd("path")

write.csv(ime_not_ears_alarms, "4_ime_not_ears_alarms.csv")
write.csv(ime_not_ears_caught, "4_ime_not_ears_caught.csv")
write.csv(ime_not_ears_diff, "4_ime_not_ears_diff.csv")