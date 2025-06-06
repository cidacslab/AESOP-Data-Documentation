

# Short description -------------------------------------------------------


#This routine creates a matrix using PHC and Dengue reported cases
#and ears results (warnings).

#Population data: 
#Fonte: IBGE. Diretoria de Pesquisas - DPE -  Coordenação Técnica do Censo 
#Demográfico - CTD

#Download: https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=35938&t=downloads
#Last accessed on: March 23, 2024.


# Packages- -----------------------------------------------------------------


pacman::p_load(tidyverse, dplyr, purr, stringr, zoo, aweek)


# Import EARS results -----------------------------------------------------


dir_parquet <- "path"

set_name <- function(name) {
  name %>%
    str_remove("\\.parquet$") %>%                    
    str_remove_all("2_ears_|_phc") %>%               
    str_replace("^c", "earsC") %>%                  
    str_replace("0\\.", "") %>%                     
    paste0("phc_", .)                                
}

files_parquet <- list.files(path = dir_parquet, 
                            pattern = "^2_ears.*\\.parquet$", 
                            full.names = TRUE)

name_files <- files_parquet %>%
  basename() %>%
  map_chr(set_name)

ears_resu <- files_parquet %>%
  map(~ arrow::read_parquet(.)) %>%
  set_names(name_files)

rm(dir_parquet, files_parquet, name_files, set_name)


# Selects only the columns of interest in the objects -----------------------


rename_cols <- function(df, name_list) {
  suf <- str_extract(name_list, "(?<=phc_ears).+")
  
  df %>%
    select(co_ibge, municipio, uf, atend_arbov, atend_totais, 
           casos_provaveis, week, epiweek, year, 
           alarm, upperbound) %>%
    rename_with(~ paste0(.x, "", suf), c("alarm", "upperbound"))
}

ears_resu <- map2(ears_resu, names(ears_resu), rename_cols)

rm(rename_cols)



# Make matrices -----------------------------------------------------------


#C1
earsC1_8w <- ears_resu$phc_earsC1_8w001 %>%
  left_join(ears_resu$phc_earsC1_8w05, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC1_8w1, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC1_8w2, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year"))


earsC1_12w <- ears_resu$phc_earsC1_12w001 %>%
  left_join(ears_resu$phc_earsC1_12w05,
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC1_12w1, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC1_12w2, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year"))


#C2
earsC2_8w <- ears_resu$phc_earsC2_8w001 %>%
  left_join(ears_resu$phc_earsC2_8w05,
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC2_8w1, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC2_8w2,
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year"))
  

earsC2_12w <- ears_resu$phc_earsC2_12w001 %>%
  left_join(ears_resu$phc_earsC2_12w05,
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year"))  %>%
  left_join(ears_resu$phc_earsC2_12w1, 
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year")) %>%
  left_join(ears_resu$phc_earsC2_12w2,
            by = c("co_ibge", "municipio", "uf", "atend_arbov", 
                   "atend_totais", "casos_provaveis", "week", 
                   "epiweek", "year"))

ears_list <- list(earsC1_8w,
                  earsC1_12w,
                  earsC2_8w,
                  earsC2_12w)

names(ears_list) <- c("earsC1_8w",
                      "earsC1_12w",
                      "earsC2_8w",
                      "earsC2_12w")

rm(ears_resu, earsC1_8w, earsC1_12w, earsC2_12w, earsC2_8w)


# Import pop data and combine it into the ears_list -----------------------


pop <- read_delim("path/POP2022_Municipios_20230622.csv",
                             delim = ";") %>%
  mutate(code_muni_ibge = paste0(cod_uf, cod_munic)) %>%
  rename(co_ibge = code_muni_ibge) %>%
  filter(!is.na(cod_uf)) %>%
  select(co_ibge, populacao_2022)

pop$co_ibge <- substr(pop$co_ibge,
              1,
              nchar(pop$co_ibge) - 1)

pop$co_ibge <- as.double(pop$co_ibge)


for(c in 1 : length(ears_list)){
  ears_list[[c]] <- left_join(ears_list[[c]],
                              pop,
                              by = "co_ibge")
};rm(c, pop)


# Classifies municipalities by size based on population_2022 --------------


for (d in 1 : length(ears_list)) {
  ears_list[[d]] <- ears_list[[d]] %>%
    mutate(porte = case_when(populacao_2022 <= 20000 ~ "pequeno_I",
                             populacao_2022 > 20000 & populacao_2022 <= 50000 ~ "pequeno_II",
                             populacao_2022 > 50000 & populacao_2022 <= 100000 ~ "medio",
                             populacao_2022 > 100000 & populacao_2022 <= 900000 ~ "grande",
                             populacao_2022 > 900000 ~ "metropole"))  
};rm(d)


# Classifies Brazil's regions ---------------------------------------------


for(e in 1 : length(ears_list)){
  ears_list[[e]] <- ears_list[[e]] %>%
    mutate(regiao = case_when(substr(co_ibge, 1, 1) == "1" ~ "Norte",
                              substr(co_ibge, 1, 1) == "2" ~ "Nordeste",
                              substr(co_ibge, 1, 1) == "3" ~ "Sudeste",
                              substr(co_ibge, 1, 1) == "4" ~ "Sul",
                              substr(co_ibge, 1, 1) == "5" ~ "Centro-Oeste",
                              TRUE ~ "Outra regi?o"))
};rm(e)


# Endemic channels based on probable cases incidence ----------------------


pop <- read_delim("path/POP2022_Municipios_20230622.csv",
                  delim = ";") %>%
  mutate(code_muni_ibge = paste0(cod_uf, cod_munic)) %>%
  rename(co_ibge = code_muni_ibge) %>%
  filter(!is.na(cod_uf)) %>%
  select(co_ibge, populacao_2022)

pop$co_ibge <- substr(pop$co_ibge,
                      1,
                      nchar(pop$co_ibge) - 1)

pop$co_ibge <- as.integer(pop$co_ibge)

arbov <- arrow::read_parquet("path/data.parquet")

arbov <- arbov %>%
  mutate(week = aweek::get_date(week = epiweek, 
                                year = ano,
                                day = 7L)) %>%
  group_by(co_ibge) %>%
  arrange(co_ibge, week) %>%
  filter(week >= "2022-10-01" & week <= "2024-03-01") %>%
  ungroup()

arbov <- left_join(arbov, 
                   pop,
                   by = "co_ibge")

incid_8sem <-  arbov %>%
  group_by(co_ibge) %>%
  arrange(co_ibge, week) %>%
  mutate(incid8sem = zoo::rollapplyr((casos_provaveis / populacao_2022), 
                                     width = 8, FUN = sum, 
                                     align = "right", 
                                     partial = TRUE, 
                                     fill = NA)) %>%
  ungroup() %>%
  select(co_ibge, week, incid8sem)


# setting incidences 0.001 and 0.003 events -------------------------------


incid_8sem <- incid_8sem %>%
  group_by(co_ibge) %>%
  arrange(co_ibge, week) %>%
  mutate(
    incid001 = 
      case_when(incid8sem >= 0.001 ~ 1,
                incid8sem < 0.001 ~ 0),
    indic003 = 
      case_when(incid8sem >= 0.003 ~ 1,
                incid8sem < 0.003 ~ 0)
  ) %>%
  ungroup()


for(f in 1 : length(ears_list)){
  ears_list[[f]] <- ears_list[[f]] %>%
    left_join(incid_8sem,
              by = c("co_ibge", "week"))
};rm(f, incid_8sem, arbov, pop)


rm(incid_8sem, arbov, pop)


# Export ------------------------------------------------------------------


output_dir <- "path/"

for(g in 1 : length(ears_list)) {
  file_path <- paste0(output_dir, "3_", names(ears_list)[g], "_phc.parquet")
  arrow::write_parquet(ears_list[[g]], file_path)
};rm(g)

rm(file_path, output_dir, ears_list)