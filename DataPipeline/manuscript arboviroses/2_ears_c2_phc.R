

# Short description -------------------------------------------------------


#This routine develops the classify_ears() function for arbovirus-related PHC 
#encounters under different baselines and adjustment parameters.

#The EARS-C2 model was adjusted as follows:

#baseline_ears = 4, 8 and 12 weeks
#alpha = 0.001, 0.05, 0.1 and 0.2


# Packages ----------------------------------------------------------------


pacman::p_load(surveillance, slider, tidyverse, aweek)


# Load the syndromic surveillance functions - EARS ------------------------


source("path/1_function_ears.R")


# Working directory -------------------------------------------------------


setwd("path")


# Primary healthcare database [PHC] ---------------------------------------


arbov <- arrow::read_parquet("data.parquet")


# 1 - Select the time series - October 1, 2022 to March 1, 2024 -----------


arbov <- arbov %>%
  mutate(week = aweek::get_date(week = epiweek, 
                                year = ano,
                                day = 7L)) %>%
  group_by(co_ibge) %>%
  arrange(week) %>%
  filter(week >= "2022-10-01" & week <= "2024-03-01")


# Run EARS-C2 baseline = 8 alpha = 0.001 -----------------------------------


ears_c2_8w001 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 11,
  baseline_ears = 8,
  alpha_ears = 0.001,
  method_ears = "C2"
)


# Run EARS-C2 baseline = 8 alpha = 0.05 ------------------------------------


ears_c2_8w05 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 11,
  baseline_ears = 8,
  alpha_ears = 0.05,
  method_ears = "C2"
)


# Run EARS-C2 baseline = 8 alpha = 0.1 -------------------------------------


ears_c2_8w1 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 11,
  baseline_ears = 8,
  alpha_ears = 0.1,
  method_ears = "C2"
)


# Run EARS-C2 baseline = 12 alpha = 0.001 ----------------------------------


ears_c2_12w001 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 15,
  baseline_ears = 12,
  alpha_ears = 0.001,
  method_ears = "C2"
)


# Run EARS-C2 baseline = 12 alpha = 0.05 -----------------------------------


ears_c2_12w05 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 15,
  baseline_ears = 12,
  alpha_ears = 0.05,
  method_ears = "C2"
)


# Run EARS-C2 baseline = 12 alpha = 0.1 ------------------------------------


ears_c2_12w1 <- classify_ears(
  arbov,
  t = week,
  data_count = atend_arbov,
  all_count = atend_totais,
  B = 15,
  baseline_ears = 12,
  alpha_ears = 0.1,
  method_ears = "C2"
)


# 3 - Export the output ---------------------------------------------------


#combine ears
ears_list <- c(
               ears_c2_8w001,
               ears_c2_8w05,
               ears_c2_8w1,
               ears_c2_12w001,
               ears_c2_12w05,
               ears_c2_12w1
               )

names(ears_list) <- c(
                      "ears_c2_8w001",
                      "ears_c2_8w05",
                      "ears_c2_8w1",
                      "ears_c2_12w001",
                      "ears_c2_12w05",
                      "ears_c2_12w1"
                      )


output_dir <- "path/"

for(g in 1 : length(ears_list)) {
  file_path <- paste0(output_dir, "2_", names(ears_list)[g], "_phc.parquet")
  arrow::write_parquet(ears_list[[g]], file_path)
};rm(g)