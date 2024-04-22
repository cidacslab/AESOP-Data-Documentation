#setwd("/mnt/opt/storage/shared/aesop/clinica/etl_aesop/codes/")
args <- commandArgs(trailingOnly = TRUE)
input_path <- args[1]
output_path <- args[2]

pacman::p_load(tidyverse, aweek)
period <- 52
alpha <- 0.05

source("00_funs.R")

aps <- arrow::read_parquet(input_path)

aps <- aps |>
  mutate(across(c(ano, epiweek), as.numeric)) |>
  arrange(co_ibge, ano, epiweek)
set_week_start("Sunday") # setting the default week_start to Sunday
# Create date from epiweek and year
aps <- aps |>
  mutate(week = get_date(week = epiweek, year = ano, day = 7L)) |>
  group_by(co_ibge) |> # downstream analysis will use grouped dfs
  arrange(week)


# start week
aps <- aps |> filter(week >= "2022-09-15")
aps <- aps |> mutate(co_ibge = as.factor(co_ibge))

# Find last week - name
last_week <- aps |>
  ungroup() |>
  filter(week == max(week)) |>
  select(week) |>
  slice_sample(n = 1) |>
  pull(week)
last_week

# Create harmonic terms
aps <- aps |>
  group_by(co_ibge) |>
  arrange(week) |>
  mutate(week_no = row_number()) |>
  dplyr::mutate(
    season = as.factor(lubridate::floor_date(week, "4 months")),
    cos1 = cos(2 * 1 * pi * week_no / period),
    sin1 = sin(2 * 1 * pi * week_no / period),
    cos2 = cos(2 * 2 * pi * week_no / period),
    sin2 = sin(2 * 2 * pi * week_no / period),
    cos3 = cos(2 * 3 * pi * week_no / period),
    sin3 = sin(2 * 3 * pi * week_no / period)
  ) |> 
  filter(atend_totais != 0) #remove random weeks without encounters (bad data)

# formulas
formula_prop_ivas <- "atend_ivas ~ season + 
  cos1 + 
  sin1 + 
  cos2 + 
  sin2 +
  offset(log(atend_totais))"


formula_prop_arbo <- "atend_arbov ~ season + 
  cos1 + 
  sin1 + 
  cos2 + 
  sin2 +
  offset(log(atend_totais))"

# IVAS

glm_prop_ivas <- aps |>
  group_by(co_ibge) |>
  nest() |>
  mutate(
    model = map(data, ~ glm_model_fun(
      df = .,
      week_length = 3,
      disease = "atend_ivas",
      formula = formula_prop_ivas
    ))
  ) |>
  select(model) |>
  unnest(cols = c(model))

glm_prop_ivas <- glm_prop_ivas |> 
  ungroup() |> 
  complete(co_ibge,week) |> 
  mutate(
    alarm_glm = case_when(
      error=="Partial data" ~ NA_real_,
      TRUE ~ alarm
    ),
    observerd = if_else(is.na(observerd),0,observerd),
    upperbound = if_else(is.na(alarm_glm), NA_integer_, upperbound),
    upperbound = as.integer(ceiling(upperbound)),
  )  |> 
  mutate(
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
  ) |> 
  group_by(co_ibge) |> 
  slice_max(order_by = week, n=3) |> 
  select(co_ibge, epiweek, epiyear, alarm_glm, observerd, upperbound) 



## Project folder
arrow::write_parquet(glm_prop_ivas, 
                 paste0(output_path,"glm_prop_ivas_",
                        "db_",
                        lubridate::epiweek(last_week),
                        "_",
                        lubridate::epiyear(last_week),
                        ".parquet"))
# ### Shared Folder
# arrow::write_parquet(glm_prop_ivas, 
#                  paste0("/mnt/opt/storage/shared/aesop/aesop_shared/resultado_ears_glm_bayes_ivas/glm_prop_ivas_", 
#                         "db_",
#                         lubridate::epiweek(last_week),
#                         "_",
#                         lubridate::epiyear(last_week),
#                         ".parquet"))



#### ARBO
glm_prop_arbo <- aps |>
  group_by(co_ibge) |>
  nest() |>
  mutate(
    model = map(data, ~ glm_model_fun(
      df = .,
      week_length = 3,
      disease = atend_arbov,
      formula = formula_prop_arbo
    ))
  ) |>
  select(model) |>
  unnest(cols = c(model))

glm_prop_arbo <- glm_prop_arbo |> 
  ungroup() |> 
  complete(co_ibge,week) |> 
  mutate(
    alarm_glm = case_when(
      error=="Partial data" ~ NA_real_,
      TRUE ~ alarm
    ),
    observerd = if_else(is.na(observerd),0,observerd),
    upperbound = if_else(is.na(alarm_glm), NA_integer_, upperbound),
    upperbound = as.integer(ceiling(upperbound)),
  )  |> 
  mutate(
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
  ) |> 
  group_by(co_ibge) |> 
  slice_max(order_by = week, n=3) |> 
  select(co_ibge, epiweek, epiyear, alarm_glm, observerd, upperbound) 

arrow::write_parquet(glm_prop_arbo, 
                 paste0(output_path,"glm_prop_arbo_", 
                        "db_",
                        lubridate::epiweek(last_week),
                        "_",
                        lubridate::epiyear(last_week),
                        ".parquet"))
# ### Shared Folder
# arrow::write_parquet(glm_prop_arbo, 
#                  paste0("/mnt/opt/storage/shared/aesop/aesop_shared/resultado_ears_glm_bayes_arbo/glm_prop_arbo_", 
#                         "db_",
#                         lubridate::epiweek(last_week),
#                         "_",
#                         lubridate::epiyear(last_week),
#                         ".parquet"))
