Web-based data
=====
Updated: 2024-05-22

A subgroup within the scope of Event-based Surveillance (EBS) [1]_ is focused on Web-based EBS (w-EBS), which pertains to events where the data is sourced from the web. This approach leverages online platforms, social media, news websites, and other internet-based resources to gather real-time information on public health events, enabling rapid detection and response to potential outbreaks and health threats.

Search Engine
-------------
TO DO

Description
^^^^^^^^^^^
TO DO

Data Dictionary
^^^^^^^^^^^^^^^
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| Field Name          | Field Label                                                 | Type       | Description                              | 
+=====================+====================================================+========+============+==========================================+
| DATE_CALENDAR_WEEK  | Date representing the first day of the week (Sunday)        | Number     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| TREND_INDICATOR     | Indicator with the search trend for the term in the period  | String     | TO DO                                    |
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| IS_PARTIAL          | Whether the data is still partial for the week in question  | String     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| SEARCH_ENGINE       | What is the search engine                                   | String     | TO DO                                    |  
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| SEARCH_KEYWORD      | Keyword or expression searched                              | String     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| UF                  | State code                                                  | String     | TO DO                                    |
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| MODEL_CAPTURE       | Version of the searched words and expressions               | String     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| TIME_FRAME          | Time interval                                               | String     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+
| CAPTURE_DATE        | Date of capture                                             | Number     | TO DO                                    | 
+---------------------+-------------------------------------------------------------+------------+------------------------------------------+


.. note::

   Dataset variables generated from Google Trends only. However, the structure will be maintained for other captures in search engines.




.. image:: web-based-search-engine-sample.png 
   :width: 612
   :height: 297 
   :align: center
   
Sample of the produced dataset.

Social Media
-------------
TO DO

Description
^^^^^^^^^^^
TO DO

Data Dictionary
^^^^^^^^^^^^^^^
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| Field Name          | Description                                                            | Type       | Format Sample                            | 
+=====================+========================================================================+============+==========================================+
| DATE                | Date of sending the message                                            | string     | 2023-04-11                               | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| OCURR_NUMBER        | Mumber of times the word or expression appears in the day              | string     | 5                                        |
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| ODL_NAME            | Name assigned to the observation being searched for in the message     | string     | SHORTNESS BREATH                         | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| ODL_TYPE            | Category or syndrome that is associated with observation               | string     | RESPIRATORY SYNDROME                     |  
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| ORIGIN_CAPTURE      | Origin of data capture                                                 | string     | TWITTER                                  | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| MODEL_CAPTURE       | version of the applied capture model                                   | string     | V1                                       |
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| MUN_IBGE_COD        | Municipality code                                                      | string     | 3304557                                  | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| MUN_NAME            | Municipality name                                                      | string     | RIO DE JANEIRO                           | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+
| GEO_LAT_LONG        | Latitude and longitude associated with the municipality's centroid     | string     | [-22.9110137,-43.344255]                 | 
+---------------------+------------------------------------------------------------------------+------------+------------------------------------------+


.. note::

   TO DO




.. image:: web-based-social-media-sample.png 
   :width: 1121
   :height: 431 
   :align: center
   
Sample of the produced dataset.



News
-------------
TO DO

Description
^^^^^^^^^^^
TO DO




.. rubric:: References

.. [1] G. J., Williams, G. M., Clements, A. C. A., & Hu, W. (2014). Internet-based surveillance systems for monitoring emerging infectious diseases. Lancet Infect Dis, 14(2), 160–168. https://doi.org/10.1016/s1473-3099(13)70244-5.


**Contributors**

+-------------------+-----------------------------------------------------------------+
| Roberto Carreiro  | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+