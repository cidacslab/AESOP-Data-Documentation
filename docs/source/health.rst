Health data
==

Primary Health Care (PHC)
--------------------------------

Description
^^^^^^^^^^^

Worldwide, various countries and health systems adopt the use of Primary Health Care (PHC) data integrated with traditional health surveillance systems to enhance sentinel surveillance and early warning of disease outbreaks capabilities (1,2).
 
Brazil's National Information System on Primary Health Care (SISAB) harbors data on all publicly funded PHC encounters in the country, coded by either the International Classification of Diseases (ICD-10) or the International Classification of Primary Care (ICPC-2) (3).SISAB is a decentralized system maintained by the Ministry of Health (MoH), with every Brazilian municipality running a version of it. Since 2016, its use has become mandatory for receiving federal funds for PHC.
 
It is estimated that the Brazilian national PHC system covers around 75% of the population (4). In 2023, the system registered an average of 39,6 million encounters per month, and all of the 5,570 municipalities registered encounters in the system.

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^
The AESOP Project maintains a SISAB database ranging from January 2017 up to now, with regular weekly updates through a specific VPN connection. Data is obtained under the permission of the MoH, and data collection is approved by the Ethical Review Board of Oswaldo Cruz Foundation - Brasília Regional Office, CAAE 61444122.0.0000.0040.


The data is aggregated and non-identified. Each line represents the weekly count of PHC encounters per reason of encounter (coded by either ICD-10 or ICPC-2), city of encounter, gender, and age group.


For establishing the early warning system based on syndromic surveillance, we grouped a broad set of codes into three categories for defining each of the following syndromes: influenza-like illness (ILI), dengue-like syndrome (DLS) and diarrhea. We aimed at guaranteeing enough sensibility for outbreak detection. The list of codes can be found at: https://github.com/cidacslab/AESOP-Data-Documentation/tree/main/DataPipeline/documentation


Data access information
^^^^^^^^^^^^^^^^^^^^^^^

Although the AESOP Project has access to weekly updates following an exclusive permission by the MoH, open access to monthly data is available through the following websites, maintained by the MoH:

- https://sisaps.saude.gov.br/painelsaps/
- https://sisab.saude.gov.br/

Data Quality Index (DQI)
^^^^^^^^^^^^^^^^^^^^^^^^

Since SISAB is an administrative database designed and maintained for governance and accountability purposes, evaluating the quality of the available data when used for early warning of outbreaks is crucial to ensure accurate interpretation of epidemiological analysis results.

We established a Data Quality Index (DQI) based on the quantitative assessment of the completeness, timeliness, and consistency of SISAB. The DQI is continuously monitored in an 8-week rolling window baseline. In this context, these three quality dimensions are defined as follows:

**Completeness**: defined as the proportion of weeks in each 8-week rolling window with registries of PHC encounters, provided there is no Consecutive Missing in the last two weeks of the 8-week rolling window.

**Timeliness**: represented by the number of weeks between the PHC encounter and the date the data was entered into the system. According to SISAB primary use, PHC encounters may be registered with up to a 4-week lag. For the early warning system purpose, such lag is unacceptable as it would yield lack of opportunity for outbreak detection.

**Consistency**: defined as a minimum number of PHC encounters registered weekly. As administrative health care databases often present with artificial aberrations in time series analysis due to events affecting health services availability and patient behavior, we considered the data to be consistent if the number of registered encounters were within the range of two standard deviations (SD) from the average number of encounters in the last 7 weeks.

In 2023, 4,458 (80%) municipalities showed completeness above 85% for at least 80% of epiweeks and 3,969 (71.2%) showed timelines above 75% for at least 80% of epiweeks. These results yielded a total of 3,713 (66.6%) with a valid DQI for issuing early warning during 80% of 2023 epiweeks. 


Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^

Data is one dataset where each line is corresponds to one Brazilian city in one month of the studied period. The variables are city population, location, number of PHC teams and facilities and the number of PHCE in each group of interest on that month . 

Limitations of PHC dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^

SISAB does not carry the entire patient’s electronic health record and, for each encounter, only one diagnostic code is retrieved in the database, leading to imprecision in classifying cases.

Moreover, detailed information on symptoms, tests, and treatments is unavailable.



Variable list for PHC database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| DB Source     | Variable          | Label                                              | Type     | Description                                                                             |
+===============+===================+====================================================+==========+=========================================================================================+
| IBGE          | municipio         | City name                                          | string   | Brazilian city name                                                                    |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| IBGE          | co_ibge           | City code                                          | numeric  | Brazilian city code                                                                    |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | ano               | Year                                               | numeric  | Year                                                                                    |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | epiweek           | Epiweek                                            | numeric  | Epiweek                                                                                 |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | atend_totais      | Total PHC Encouters                                | numeric  | Total PHC Encounters in Brazilian cities                                                |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | atend_ivas        | Upper Respiratory Infections related symptoms encounters | numeric  | Upper Respiratory Infections related symptoms encounters in Brazilian cities            |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | atend_arbov       | Arbovirus Infection related symptoms encounters    | numeric  | Arbovirus Infection related symptoms in Brazilian cities                                |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| SISAB         | faixa_etaria      | Age range                                          | string   | Age range from individuals that were attended in PHC                                    |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| e-Gestor APS  | pc_cobertura_sf   | Estimated coverage of family health teams          | numeric  | Estimated coverage of family health teams                                                |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| e-Gestor APS  | pc_cobertura_ab   | Estimated coverage of all PHC Teams                | numeric  | Estimated coverage of all PHC Teams                                                     |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| IBGE          | cod_rgiimediata   | Immediate Region code                              | numeric  | Groupings of municipalities that have as their main reference the urban network and have a local urban center as a basis |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| IBGE          | nome_rgi          | Immediate Region name                              | string   | Groupings of municipalities that have as their main reference the urban network and have a local urban center as a basis |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| IBGE          | cod_rgint         | Intermediate Geographical Regions codes            | numeric  | Organize the Immediate Regions in the territory based on a region that provides more complex services, such as specialized medical services or large universities |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+
| IBGE          | nome_rgint        | Intermediate Geographical Regions names            | string   | Organize the Immediate Regions in the territory based on a region that provides more complex services, such as specialized medical services or large universities |
+---------------+-------------------+----------------------------------------------------+----------+-----------------------------------------------------------------------------------------+




.. rubric:: References

(1) Bagaria J, Jansen T, Marques DFP, Hooiveld M, McMenamin J, de Lusignan S, Vilcu AM, Meijer A, Rodrigues AP, Brytting M, Mazagatos C, Cogdale J, van der Werf S, Dijkstra F, Guiomar R, Enkirch T, Valenciano M, I-MOVE-COVID-19 study team. Rapidly adapting primary care sentinel surveillance across seven countries in Europe for COVID-19 in the first half of 2020: strengths, challenges, and lessons learned. Euro Surveill. 2022;27(26):pii=2100864. doi:10.2807/1560-7917.ES.2022.27.26.2100864.

(2) Prado NMBL, Biscarde DGDS, Pinto Junior EP, Santos HLPCD, Mota SEC, Menezes ELC, Oliveira JS, Santos AMD. Primary care-based health surveillance actions in response to the COVID-19 pandemic: contributions to the debate. Cien Saude Colet. 2021l;26(7):2843-2857. doi: 10.1590/1413-81232021267.00582021.

(3) Cerqueira-Silva T, Oliveira JF, Oliveira VA, Florentino PTV, Sironi A, Penna GO, Ramos PIP, Boaventura VS, Barral-Netto M, Marcilio I. Early warning system using primary healthcare data in the post-COVID-19-pandemic era: Brazil nationwide case-study. Pre-print available at medRxiv: doi: 10.1101/2023.11.24.23299005

(4) Sellera PEG, Pedebos LA, Harzheim E, Medeiros OL de, Ramos LG, Martins C, D’Avila OP. Monitoramento e avaliação dos atributos da Atenção Primária à Saúde em nível nacional: novos desafios. Ciênc Saúde Coletiva. 2020;25(4):1401–12. doi:10.1590/1413-81232020254.36942019



**Contributors**

+-------------------+-----------------------------------------------------------------+
| George Barbosa    | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+
| Izabel Marcilio   | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+
| Juracy Bertoldo   | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+
| Pilar Veras       | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+
| Vinicius Oliveira | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+



