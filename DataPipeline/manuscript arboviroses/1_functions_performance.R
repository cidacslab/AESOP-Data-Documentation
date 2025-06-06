

# Short description -------------------------------------------------------


#This routine was adapted from:

#Nekorchuk, D. M., et al (2021). Comparing malaria early detection methods in a 
#declining transmission setting in northwestern Ethiopia. BMC public health, 
#21(1), 788.


# fun_ears_total ----------------------------------------------------------


fun_ears_total <- function(data_aps, 
                           regex_state, 
                           pre_week_search,
                           method,
                           alpha1, 
                           week_start,
                           week_end,
                           baseline) {
  ufstate <- regex_state
  
  aps_base <- data_aps %>%
    filter(
      str_detect(cod_rgi, ufstate)
    ) %>%
    filter(
      week > week_start,
      week < week_end
    ) %>%
    group_by(week) %>%
    summarise(
      n_total = sum(n_total),
      n_selected = sum(n_selected)
    ) %>%
    arrange(week) %>%
    mutate(
      time = row_number(),
      epi_week = lubridate::epiweek(week),
      epi_year = lubridate::epiyear(week)
    ) %>%
    filter(!is.na(week),
           n_total!=0)
  
  datsts <- sts(
    observed = aps_base$n_selected,
    start = c(min(lubridate::epiyear(aps_base$week)), 
              lubridate::epiweek(min(aps_base$week))), frequency = 52,
    epoch = aps_base$week,
    epochAsDate = T
  )
  control_ears <- list(
    method = method,
    alpha = alpha1,
    baseline = baseline,
    minSigma=0.5
  )
  ears_aps <- earsC(datsts, control = control_ears)
  
  
  # ears_aps@state <- ears_srag@alarm - it break sometimes
  tidy_aps <- tidy.sts(ears_aps)
  return(list(
    tidy_aps = tidy_aps
  ))
}


# calculate_event_overlaps ------------------------------------------------


calculate_event_overlaps <- function(algo_events, algo_alarms){
  for(w in 1:length(algo_events)){
    
    if (nrow(algo_events[[w]]) == 0) next
    
    algo_events[[w]][, "num_catches"] <- 0
    algo_events[[w]][, "first_alarm"] <- as.Date(NA)
    algo_events[[w]][, "caught"] <- FALSE
    algo_events[[w]][, "timely_wks"] <- difftime(NA, NA, units = "weeks") %>% as.integer() #as.period(units = "week")
    for(e in 1:nrow(algo_events[[w]])){
      
      alarm_catch <- 0
      first_alarm <- as.Date(NA)
      
      
      if (nrow(algo_alarms[[w]]) > 0) {
        for(a in 1:nrow(algo_alarms[[w]])){
          overlap_this_row <- int_overlaps(algo_events[[w]][[e, "search_intv"]],  
                                           algo_alarms[[w]][[a, "intv"]])
          alarm_catch <- alarm_catch + overlap_this_row
          first_this_row <- if (overlap_this_row) algo_alarms[[w]][[a, "start_dt"]] else as.Date(NA)
          first_alarm <- min(first_alarm, 
                             first_this_row, 
                             na.rm = TRUE)
        }
      }
      
      
      algo_events[[w]][e, "num_catches"] <- alarm_catch
      algo_events[[w]][e, "first_alarm"] <- first_alarm
      #calculations from info
      algo_events[[w]][e, "caught"] <- if (algo_events[[w]][[e, "num_catches"]] > 0) TRUE else FALSE
      algo_events[[w]][e, "timely_wks"] <- if (algo_events[[w]][[e, "caught"]]) {
        difftime(algo_events[[w]][[e, "first_alarm"]], 
                 algo_events[[w]][[e, "start_dt"]], 
                 units = "weeks") %>% as.integer()
      } else {
        NA_integer_
      }
      
    }
  }
  algo_events
}


# events_caught -----------------------------------------------------------


events_caught <- function(df_event_overlaps){
  if(nrow(as.data.frame(df_event_overlaps))==0){
    data.frame(num_events=NA,
               num_caught=NA,
               perc_caught=NA,
               perc_no_caught=NA,
               perc_missed=NA)
  }else{
  df_event_overlaps %>% 

    do.call(rbind, .) %>% 
    
    summarize(num_events = n(),
              num_caught = sum(caught), #VP
              num_no_caugth = sum(caught == F), #FN 
              perc_caught = num_caught / num_events * 100, #% VP
              perc_no_caught = num_no_caugth / num_caught * 100, #FN
              perc_missed = 100 - perc_caught)
  }
}  


# events_timely -----------------------------------------------------------


events_timely <- function(df_event_overlaps){
  if(nrow(as.data.frame(df_event_overlaps))==0){
    data.frame(preevent = NA,
              preevent_prc = NA,
              no_delay = NA,
              no_delay_prc = NA,
              minor_delay = NA,
              minor_daly_prc = NA,
              delayed = NA,
              delayed_prc = NA,
              median_delay = NA,
              mean_delay = NA,
              not_delayed = NA,
              not_delayed_prc = NA)
  }else{
  freqs <- df_event_overlaps %>%
    do.call(rbind, .) %>% 
    filter(caught == TRUE) %>% 
    select(timely_wks) %>% 
    #frequencies of each value
    table() %>%
    as.data.frame()
  

  if (nrow(freqs) < 1) {
    freqs <- data.frame("weeks" = 0, "freq" = 0)
  } else {

    colnames(freqs) <- c("weeks", "freq")

    freqs$weeks <- as.numeric(as.character(freqs$weeks))
  }
  

  freqs %>% 
    summarize(preevent = sum(freq[weeks<0]),
              preevent_prc = preevent / sum(freq) * 100,
              no_delay = sum(freq[weeks==0]),
              no_delay_prc = no_delay / sum(freq) * 100,
              minor_delay = sum(freq[weeks==1]),
              minor_daly_prc = minor_delay / sum(freq) * 100,
              delayed = sum(freq[weeks>=2]),
              delayed_prc = delayed / sum(freq) * 100,
              median_delay = median(freq, na.rm = TRUE),
              mean_delay = mean(freq, na.rm = TRUE),
              not_delayed = preevent + no_delay + minor_delay,
              not_delayed_prc = not_delayed / sum(freq) * 100)
  }
}


# calculate_alarm_overlaps ------------------------------------------------


calculate_alarm_overlaps <- function(algo_alarms, algo_events){

  for(w in 1:length(algo_alarms)){

    if (nrow(algo_alarms[[w]]) == 0) next
    

    algo_alarms[[w]][, "num_events"] <- 0
    algo_alarms[[w]][, "with_event"] <- FALSE
    
    for(a in 1:nrow(algo_alarms[[w]])){

      event_catch <- 0
      

      if (nrow(algo_events[[w]]) > 0) {

        for(e in 1:nrow(algo_events[[w]])){
          overlap_this_row <- int_overlaps(algo_alarms[[w]][[a, "intv"]],  
                                           algo_events[[w]][[e, "search_intv"]])
          event_catch <- event_catch + overlap_this_row
        }
      }
      
      
      algo_alarms[[w]][a, "num_events"] <- event_catch
      
      algo_alarms[[w]][a, "with_event"] <- if (algo_alarms[[w]][[a, "num_events"]] > 0) TRUE else FALSE
      
    }
  }
  algo_alarms
}


# alarms_events -----------------------------------------------------------


alarms_events <- function(df_alarm_overlaps) {
  
  # Unir os data.frames de forma segura
  alarm_over_bind <- bind_rows(df_alarm_overlaps)
  
  # Se houver pelo menos um alarme, calcular métricas
  if (nrow(alarm_over_bind) > 0) {
    
    alarm_event_results <- alarm_over_bind %>%
      summarize(
        num_alarms = n(),
        num_truepos = sum(with_event, na.rm = TRUE),  # VP
        num_trueneg = sum(!with_event, na.rm = TRUE), # VN
        perc_truepos = if_else(num_alarms > 0, num_truepos / num_alarms * 100, NA_real_),
        perc_falsepos = if_else(num_alarms > 0, 100 - perc_truepos, NA_real_),
        perc_trueneg = if_else(num_alarms > 0, num_trueneg / num_alarms * 100, NA_real_)
      )
    
  } else {
    
    # Caso sem dados, preencher com NA
    alarm_event_results <- tibble(
      num_alarms = NA_real_,
      num_truepos = NA_real_,
      num_trueneg = NA_real_,
      perc_truepos = NA_real_,
      perc_falsepos = NA_real_,
      perc_trueneg = NA_real_
    )
  }
  
  return(alarm_event_results)
}


# id_alarms ---------------------------------------------------------------


id_alarms <- function(algo_df, algo_rle){

  algo_df %>%

    mutate(runID = with(algo_rle, { rep(seq_along(lengths), lengths)})) %>%

    filter(alarm == TRUE) %>%

    mutate(alarmID = match(runID, unique(runID))) %>%

    group_by(alarmID) %>%
    summarize(start_dt = min(epoch),
              end_dt = max(epoch)) %>%
    mutate(intv = interval(start_dt, end_dt))
}


# id_events ---------------------------------------------------------------


id_events <- function(algo_df, algo_rle, pre_week_search){
  
  algo_df %>%
  
    mutate(runID = with(algo_rle, { rep(seq_along(lengths), lengths)})) %>%
  
    filter(state == TRUE) %>%
  
    mutate(eventID = match(runID, unique(runID))) %>%
    
    group_by(eventID) %>%
    summarize(start_dt = min(epoch),
              end_dt = max(epoch)) %>%
    mutate(intv = interval(start_dt, end_dt),
           search_start_dt = start_dt - as.difftime(pre_week_search, unit = "weeks"),
           search_intv = interval(search_start_dt, end_dt))
}


# calculate_overlaps ------------------------------------------------------


calculate_overlaps <- function(algo_dfs, pre_week_search){
  
  
  algo_alarm_rles <- lapply(algo_dfs, function(x) rle(x$alarm))
  algo_event_rles <- lapply(algo_dfs, function(x) rle(x$state))
  
  
  algo_alarms <- mapply(FUN = id_alarms, 
                        algo_dfs, 
                        algo_alarm_rles, 
                        SIMPLIFY = FALSE)
  algo_events <- mapply(FUN = id_events, 
                        algo_dfs, 
                        algo_event_rles, 
                        MoreArgs = list(pre_week_search), 
                        SIMPLIFY = FALSE)
  
  
  algo_event_overlaps <- calculate_event_overlaps(algo_events, algo_alarms)
  
  algo_alarm_overlaps <- calculate_alarm_overlaps(algo_alarms, algo_events)
  
  
  return(list(algo_event_overlaps, algo_alarm_overlaps))
}