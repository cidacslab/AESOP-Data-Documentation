
args <- commandArgs(trailingOnly = TRUE)
input_path <- args[1]
output_path <- args[2]

setwd("/home/juracy/codigos_2021/fiocruz/aesop/modelos_R/modelos/")
pacman::p_load(surveillance, slider, tidyverse, aweek)

source("00_funs.R")

#semana 11
aps <- arrow::read_parquet(input_path)

aps <- aps |>
  mutate(across(c(ano, epiweek), as.numeric)) |>
  arrange(co_ibge, ano, epiweek)
set_week_start("Sunday") # setting the default week_start to Sunday
# Create date from epiweek and year
aps <- aps |>
  mutate(week = get_date(week = epiweek, year = ano, day = 7L)) |>
  group_by(co_ibge) |> #downstream analysis will use grouped dfs
  arrange(week)

# Extract last week
last_week <- aps |>
  ungroup() |>
  filter(week == max(week)) |>
  select(week) |>
  slice_sample(n = 1) |>
  pull(week)
filter_week <- last_week - 106
aps <- aps |> filter(week >= filter_week)



########### IVAS ############

result_ears_ivas <- classify_ears(aps,
  t = week,
  data_count = atend_ivas,
  all_count = atend_totais,
  B = 11, # current week + 2 guard + 8 baseline
  baseline_ears = 8,
  alpha_ears = 0.05,
  method_ears = "C2"
)

result_final_ivas <- result_ears_ivas |>
  mutate(alarm_ears = case_when(
    alarm == "TRUE" ~ "1",
    alarm == "FALSE" ~ "0",
    alarm == "No data" ~ NA_character_
  ),
  observed = if_else(is.na(observed), atend_ivas, observed)) |>
  select(alarm_ears, upperbound, observed, municipio, week, co_ibge) |>
  group_by(co_ibge) |>
  arrange(week) |>
  slice_max(week, n = 3)  # get last 3 weeks

## Harmonize classes
result_final_ivas <- result_final_ivas |> 
  mutate(
    alarm_ears = as.integer(alarm_ears),
    upperbound = as.integer(ceiling(upperbound)),
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
    ) |> 
  select(-week)

### Project folder
arrow::write_parquet(result_ears_ivas, 
                 paste0(output_path,"ears_ivas_", 
                        "db_",
                        lubridate::epiweek(last_week),
                        "_",
                        lubridate::epiyear(last_week),
                        ".parquet"))
### Shared Folder
#arrow::write_parquet(result_final_ivas, 
#          paste0(output_path,"/ears_ivas_", 
#                 "db_",
#                 lubridate::epiweek(last_week),
#                 "_",
#                 lubridate::epiyear(last_week),
#                 ".parquet"))




########### ARBOV ###########

result_ears_arbo <- classify_ears(aps,
                                  t = week,
                                  data_count = atend_arbov,
                                  all_count = atend_totais,
                                  B = 11, # current week + 2 guard + 8 baseline
                                  baseline_ears = 8,
                                  alpha_ears = 0.05,
                                  method_ears = "C2"
)

result_final_arbo <- result_ears_arbo |>
  mutate(alarm_ears = case_when(
    alarm == "TRUE" ~ "1",
    alarm == "FALSE" ~ "0",
    alarm == "No data" ~ NA_character_
  ),
  observed = if_else(is.na(observed), atend_arbov, observed)) |>
  select(alarm_ears, upperbound, observed, municipio, week, co_ibge) |>
  group_by(co_ibge) |>
  arrange(week) |>
  slice_max(week, n = 3)  # get last 3 weeks

## Harmonize classes
result_final_arbo <- result_final_arbo |> 
  mutate(
    alarm_ears = as.integer(alarm_ears),
    upperbound = as.integer(ceiling(upperbound)),
    upperbound = replace_na(upperbound, 0L),
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
  ) |> 
  select(-week)


### Project folder
arrow::write_parquet(result_ears_arbo, 
                     paste0(output_path,"ears_arbo_", 
                        "db_",
                        lubridate::epiweek(last_week),
                        "_",
                        lubridate::epiyear(last_week),
                        ".parquet"))
### Shared Folder
# arrow::write_parquet(result_final_arbo, 
#                  paste0("/media/juracy/dados_2/projetos/aesopdata/aesop_s3_output/semana_11_2024/modelos_R/ears_arbo_", 
#                         "db_",
#                         lubridate::epiweek(last_week),
#                         "_",
#                         lubridate::epiyear(last_week),
#                         ".parquet"))









