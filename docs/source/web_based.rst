Web-based data
=====
Updated: 2024-05-22

A subgroup within the scope of Event-based Surveillance (EBS) [1]_ is focused on Web-based EBS (w-EBS), which pertains to events where the data is sourced from the web. This approach leverages online platforms, social media, news websites, and other internet-based resources to gather real-time information on public health events, enabling rapid detection and response to potential outbreaks and health threats.

However, web-based data has challenges that need to be considered, among which we highlight:

      * Data Integrity: Maintaining the veracity and accuracy of the data.
      * Noise Filtration and Relevance: Developing advanced methods to filter out irrelevant content and pinpoint pertinent information.
      * Sampling Bias: Addressing the variation in web-based (e.g. social media and internet) usage across different populations to avoid sampling bias.
      * Technological Tools: Using natural language processing, machine learning, and big data analytics to transform unstructured data into actionable insights.
      * Integration with traditional initiatives: How to do it and obtain results to generate warnings/alerts.

Therefore, within the scope of Aesop, we consider that web-based data is for context, being a "side-car" in the process of evaluating a notice.

Search Engine
-------------

Description
^^^^^^^^^^^
Search engines are considered in studies as a promising source for the early detection of events that may represent potential public health issues [TO DO]. Within the scope of the Aesop project, search engines serve as a "side-car" data source, meaning they require another primary source to guide the alert. Search engines such as Google, Bing, Yahoo, and others are valuable for understanding population search patterns, which can indicate trends of interest related to health topics that contribute to epidemiological surveillance.

On one hand, this is an opportune process that can aid decision-making by enabling the issuance of an alert when something outside the norm (an anomaly) is detected [TO DO]. Search engine data can reveal real-time insights into public health concerns by identifying spikes in search queries for symptoms, diseases, or other health-related topics. This proactive approach allows for a more responsive and dynamic public health monitoring system.

Thus, search engines, while secondary, play a critical contextual role in the overall surveillance framework, providing a complementary layer of data that enhances the ability to detect and respond to public health threats more swiftly.

Data access information
^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Limitations of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
Datasets generated from Google Trends have limitations regarding the attribution of searches to areas smaller than states. Therefore, initially, the datasets are associated with states.

It is crucial to integrate search engine data with other traditional and validated data sources to ensure accuracy and reliability. This integration helps mitigate issues such as data noise, sampling bias, and the relevance of the information gathered. Employing advanced technologies like natural language processing, machine learning, and big data analytics can enhance the ability to filter and analyze search engine data, transforming it into actionable insights.

Additionally, cultural factors, internet access, and digital literacy among the population must be considered. Variations in these areas can influence the volume and type of search queries, potentially affecting the representativeness of the data. Populations with limited internet access or lower levels of digital literacy might be underrepresented in search engine data, leading to biases. Understanding these limitations is essential for accurately interpreting the data and ensuring it complements other surveillance methods effectively.

Furthermore, while search engine data offers universal accessibility and the potential to be obtained independently of the health system, this advantage is conditioned by the cultural and socio-economic context of the population. Differences in health-seeking behaviors, language, and economic status can impact how individuals use search engines for health information. Recognizing these factors is crucial to leveraging search engine data effectively and ensuring it provides a meaningful contribution to public health surveillance.

Data dictionary
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

Description
^^^^^^^^^^^
TO DO

Data access information
^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Limitations of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Data dictionary
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

Description
^^^^^^^^^^^
TO DO

Data access information
^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Limitations of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^
TO DO

Data dictionary
^^^^^^^^^^^^^^^
TO DO




.. rubric:: References

.. [1] G. J., Williams, G. M., Clements, A. C. A., & Hu, W. (2014). Internet-based surveillance systems for monitoring emerging infectious diseases. Lancet Infect Dis, 14(2), 160–168. https://doi.org/10.1016/s1473-3099(13)70244-5.
.. [2] G. J., Williams, G. M., Clements, A. C. A., & Hu, W. (2014). Internet-based surveillance systems for monitoring emerging infectious diseases. Lancet Infect Dis, 14(2), 160–168. https://doi.org/10.1016/s1473-3099(13)70244-5.



**Contributors**

+-------------------+-----------------------------------------------------------------+
| Roberto Carreiro  | Center for Data and Knowledge Integration for Health (CIDACS),  |
|                   | Instituto Gonçalo Moniz, Fundação Oswaldo Cruz, Salvador, Brazil|
+-------------------+-----------------------------------------------------------------+