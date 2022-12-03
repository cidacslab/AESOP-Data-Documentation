Socioeconomic determinants
=====

Brazilian deprivation index (IBP)
--------------------------------

Description
^^^^^^^^^^^

It provides deprivation measures for each Brazilian municipality based on the 2010 Brazilian census data. It is used to evaluate health inequalities across the country. The 2010 Brazilian Census social and economic estimatimations are the basis for calculating the deprivation measure, available at [1]_ and [2]_. 

The IBP index combines three factors: 

1. the percentage of families with income per capita below half of the minimum wage; 
2. the percentage of illiterate people older than 7 years old; 
3. the percentage of people without adequate access to drinkable water, sewage, garbage collection, bathroom, or shower;

A complete documentation about the construction of the index is presented in [2]_. The original data source and visualization can be found in [1]_ and [2]_.

Data access information
^^^^^^^^^^^^^^^^^^^^^^^

The data and documentation are available at the University of Glasgow [2]_. The data and this report are distributed under the Creative Commons Share-Alike license (CC BY-SA 4.0) and can be freely used by researchers, policymakers, or members of the public.

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^
The data can be download in [1]_ or [2]_. The database describe the deprivation index for each municipality in 2010. No other update are available in the institutions that created it.

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^

The IBP for Brazilian municipalities dataset has a total of 15 columns (variables) and shows a total of 5566 registries (rows) and a size of 734 KB. 

Limitations of IBP dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^

The IBP dataset includes only 3 measures of deprivation excluding others like employment, crime, health, education, and access to public services. It is also exclusively related to the year 2010 making comparison along time impracticable. The different population and ethnic groups (eg, indigenous peoples, quilombolas, riverside populations) are also not considered and there are some biases inherent to rural areas. 

Variable list for IBP database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| Original field name | Field label                                        | Type   | Category      | Description                           | 
+=====================+====================================================+========+===============+=======================================+
| ip_cd_d             | Localization code, in this case                    | Number | Uncategorized | Localization code, in this case it is | 
+                     +                                                    +        +               +                                       +  
|                     | it is the same as the city.                        |        |               | the same as the city.                 |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_cd_m             | City code                                          | Number | Uncategorized | city code                             | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_nm_f             | State name                                         | String | Uncategorized | State name                            |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_nm_r             | Region name                                        | String | Uncategorized | Region name                           | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_cd_f             | State acronym                                      | String | Uncategorized | State acronym                         |  
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_vl_f             | State code                                         | Number | Uncategorized | State code                            | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_vl_p             | Population according to IBGE (Brazilian            | Number | Uncategorized | Population according to IBGE  2010    |
+                     +                                                    +        +               +                                       +
|                     | Institute of Geography and Statistics) 2010 census |        |               | census                                |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_nm_m             | city name                                          | String | Uncategorized | City name                             | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_vl_n             | Value of the deprivation index                     | Number | Uncategorized | Value of the deprivation index        | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_dcl_             | Decile of the deprivation index                    | Number | Uncategorized | Decile of the deprivation index       | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_qntl_n           | Quintile of the deprivation index                  | Number | Uncategorized | Quintile of the deprivation index     | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_prcnt_r          | Percentage of people with per capita               | Number | Uncategorized | Percentage of people with per capita  | 
+                     +                                                    +        +               +                                       +   
|                     | income below 1/2 minimum wage                      |        |               | income below 1/2 minimum wage         |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_prcnt_d          | Percentage of illiterate people over               | Number | Uncategorized | Percentage of illiterate people over  | 
|                     | 7 years old                                        |        |               | 7 years old.                          |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_prcnt_m          | Percentage of population in                        | Number | Uncategorized | Percentage of population in           | 
|                     | inappropriate homes.                               |        |               | inappropriate homes.                  |
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+
| ip_cd_c             | empty/unknown                                      |        |               |                                       | 
+---------------------+----------------------------------------------------+--------+---------------+---------------------------------------+

To facilitate visualisation, we have also provided a data explorer that allows users to view the first rows the dataset along with metadata, including column descriptions, variable type, and variable harmonisation where applicable. This also allows broader re-use of this dataset, particularly since the original descriptors and data dictionaries are usually only available in Portuguese. Please, see https://pamepi.rondonia.fiocruz.br/en/ibp_en.html. 

.. note::

  the `Platform for analytical models in epidemiology - PAMEpi <https://pamepi.rondonia.fiocruz.br/en/index_en.html.>`_ offers support in the documentation and collection of this database. More details in [3]_, [4]_ and [5]_.

.. rubric:: References

.. [1] CIDACS. (2020, 09 01). IBP. Retrieved October 07, 2022, from https://cidacs.bahia.fiocruz.br/ibp/painel/.
.. [2] Allik, M., Ramos, D., Agranonik, M., Pinto Júnior, E.P., Ichihara, M.Y., Barreto, M.L., Leyland, A.H. and Dundas, R., 2020. Developing a small-area deprivation measure for Brazil. See https://researchdata.gla.ac.uk/980/.
.. [3] Platform for analytical models in epidemiology - PAMEpi. https://pamepi.rondonia.fiocruz.br/en/index_en.html. Accessed: February 25, 2022.
.. [4] GitHub directory - PAMepi/PAMepi-scripts-datalake: v1.0.0 (v1.0.0). Zenodo. . https://doi.org/10.5281/zenodo.6384641. Accessed: February 25, 2022.
.. [5] da Silva, N.B., Valencia, L.I.O., Ferreira, A., Pereira, F.A., de Oliveira, G.L., Oliveira, P.F., Rodrigues, M.S., Ramos, P.I. and Oliveira, J.F., 2022. Brazilian COVID-19 data streaming. arXiv preprint arXiv:2205.05032.
