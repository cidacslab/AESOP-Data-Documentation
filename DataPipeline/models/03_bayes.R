args <- commandArgs(trailingOnly = TRUE)
input_path <- args[1]
output_path <- args[2]

#setwd("/mnt/opt/storage/shared/aesop/clinica/etl_aesop/codes/")
source("00_funs.R")
pacman::p_load(aweek, tidyverse, brms, tidybayes, lubridate, future, furrr) # add cmdstanr remotes::install_github("stan-dev/cmdstanr")
#remotes::install_github("stan-dev/cmdstanr")
#library(cmdstanr)
#install_cmdstan()
# date of run
format(Sys.Date(), "%Y_%m_%d")
aps <- arrow::read_parquet(input_path)

# Fix to use update with backend cmdstanr
# compile model before function
mod <- brms::brm(data_count ~ t + offset(log(all_count)),
  family = negbinomial(),
  data = data.frame(data_count = 1, t = 1, all_count = 1),
  backend = "cmdstanr",
  chains = 0,
  seed = 7
)

set.seed(7)
# fix problems with update
fname <- paste0("fit_cmdstanr_", sample.int(.Machine$integer.max, 1))
# end fix
set_week_start("Sunday") # setting the default week_start to Sunday
aps <- aps |> mutate(week = get_date(week = epiweek, year = ano, day = 7L))

# Extract last week
last_week <- aps |>
  ungroup() |>
  filter(week == max(week)) |>
  select(week) |>
  slice_sample(n = 1) |>
  pull(week)
filter_week <- last_week - 106
aps <- aps |> filter(week >= filter_week)


aps <- aps |>
  group_by(co_ibge) |>
  arrange(week)


# plan(multisession(workers = 4))
# bayes_city <- classify_trend(df=aps, t= week, all_count = atend_totais, data_count = atend_ivas, B=8)

cities_split <- split(aps, aps$co_ibge)

plan(multisession, workers = 15) # 20 to interactive sessions , padrão 24 cores, para juracy pc vou usar 15
# furrr_options(seed=T)
bayes_ivas <- furrr::future_map_dfr(cities_split,
  ~ classify_trend(
    df = .x,
    t = week,
    all_count = atend_totais,
    data_count = atend_ivas,
    B = 8
  ),
  .options = furrr_options(seed = T)
)

bayes_ivas <- bayes_ivas |>
  select(co_ibge, week, pos) |>
  group_by(co_ibge) |>
  arrange(week) |>
  slice_max(n = 3, order_by = week) |>
  rename(prob_gro_trend = pos) |>
  mutate(
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
  ) |>
  select(-week)


## Project folder
arrow::write_parquet(
  bayes_ivas,
  paste0(
    output_path,"bayes_ivas_",
    "db_",
    lubridate::epiweek(last_week),
    "_",
    lubridate::epiyear(last_week),
    ".parquet"))
### Shared Folder
# arrow::write_parquet(
#   bayes_ivas,
#   paste0(
#     "/mnt/opt/storage/shared/aesop/aesop_shared/resultado_ears_glm_bayes_ivas/bayes_ivas_",
#     "db_",
#     lubridate::epiweek(last_week),
#     "_",
#     lubridate::epiyear(last_week),
#     ".parquet"))

##### Arbo ####
bayes_arbo <- furrr::future_map_dfr(cities_split,
  ~ classify_trend(
    df = .x,
    t = week,
    all_count = atend_totais,
    data_count = atend_arbov,
    B = 8
  ),
  .options = furrr_options(seed = T)
)


bayes_arbo <- bayes_arbo |>
  select(co_ibge, week, pos) |>
  group_by(co_ibge) |>
  arrange(week) |>
  slice_max(n = 3, order_by = week) |>
  rename(prob_gro_trend = pos) |>
  mutate(
    epiweek = lubridate::epiweek(week),
    epiyear = lubridate::epiyear(week)
  ) |>
  select(-week)


## Project folder
arrow::write_parquet(
  bayes_arbo,
  paste0(
    output_path,"bayes_arbo_",
    "db_",
    lubridate::epiweek(last_week),
    "_",
    lubridate::epiyear(last_week),
    ".parquet"))
### Shared Folder
# arrow::write_parquet(
#   bayes_arbo,
#   paste0(
#     "/mnt/opt/storage/shared/aesop/aesop_shared/resultado_ears_glm_bayes_arbo/bayes_arbo_",
#     "db_",
#     lubridate::epiweek(last_week),
#     "_",
#     lubridate::epiyear(last_week),
#     ".parquet"))
