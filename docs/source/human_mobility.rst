Human Mobility
==============

Road and Fluvial network
--------------------------------

Description
^^^^^^^^^^^

In 2016, the Network Agency of the IBGE released a database to assess the accessibility of Brazilian municipalities through public transportation [1]_. The primary focus of the data is to identify the most and least accessible areas within the country. 

The data, provided by the IBGE, includes information on weekly trip frequency between pairs of municipalities, vehicle types, travel durations, and ticket costs. Much of this information was obtained from bus companies through questionnaires completed at bus terminals. For municipalities without bus stations, alternative contact points were used, such as ticket offices in commercial establishments, bus stops under municipal administrations, city halls, and direct communication  with companies. However, relying solely on formal bus companies was insufficient to represent the true accessibility of cities, as there are municipalities where such companies are absent and no bus lines operate. As a result, informal and alternative modes of transportation (vans, station wagons, mini-buses, etc.) were also included in the research. These informal/alternative carriers typically step in to provide transportation in areas where official companies are unavailable. The data provided by these alternative transportation modes is of declaratory nature, with the database categorized into those registered in the National Register of Legal Entities (CNPJ) and those that do not disclose such information.
 
Recognizing the diversity of transportation options and the uneven distribution of road networks, data on water transport, predominantly found in the North Region of Brazil, was also gathered. Similar to road transport, formal companies operating at waterway terminals, boat cooperatives, and individual boat operators, with varying levels of formalization, were included in the data collection process.

Data access information
^^^^^^^^^^^^^^^^^^^^^^^

The data is openly available on the IBGE website and documentation is available at the 2016 roads and fluvial connections report [1]_. 

Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^

This data does not need to be updated unless a newer report is published. Data is open access in the IBGE websites, particularly on the following link:

- http://geoftp.ibge.gov.br/organizacao_do_territorio/redes_e_fluxos_geograficos/

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^

The data gathered by the IBGE provides estimates of the weekly frequency of a standard normalized vehicle capacity. To have a normalized unity of measure of vehicle mobility between cities, first it was estimated the weekly frequency of vehicles by adding the number of weekly departures between each pair of  municipalities. For connection pairs with only quarterly or monthly frequency, the sum of the departure frequencies is adjusted by multiplying it by 0.5 and 0.25, respectively, in order to align with the weekly frequency.
 
Since different types of vehicles have varying transport capacities, they are also assigned weights. Buses are considered as the standard measure (assigned a 
value of 1), while van and car frequencies are multiplied by 0.25. Regarding waterway vehicles, flying boats have their frequencies multiplied by 0.25, 
speedboats and catamarans are treated as analogous to buses (value 1), boats are multiplied by 1.5, and ships by 2. This approach enables us to estimate the 
number of passengers departing from one city to another, based on an average estimate of the number of passengers on a road bus. In this work we assume an 
average of 60 passengers per bus.
 
The database provided by IBGE is for the year 2016. It consists of 23 columns and 65,640 records (rows), in xlsx format, with a size of 9.2MB (dataset original 
name: Base_de_dados_ligacoes_rodoviarias_e_hidroviarias_2016.xlsx). The variables relevant to the project's analysis of road and fluvial mobility are listed in 
below.

Limitations
^^^^^^^^^^^

Uncertainties surrounding the availability and regularity of transportation services is still a problem in some Brazilian cities. Some municipalities lack 
public transportation altogether, and their population relies solely on private transport options. In other cases, municipalities have weaker and more tenuous 
integrated transportation systems, they do not meet the necessary temporal or spatial requirements for inclusion in IBGE research. Consequently, collecting
reliable information about their transportation situation becomes challenging.

Another limitation of the data is the representation of connections between municipalities that share the same boundary or that are geographically closed. 
These municipalities share inter municipal transportations that also operates in another municipality. Examples will be shown later. The use of the NDTI 
database is one option to overcome this difficulty.

Variable list 
^^^^^^^^^^^^^

List of variables extracted from the IBGE database to describe the intercity road and  fluvial mobility in Brazil.

+---------------------+--------------------------------------------------------------------------+
| Original field name | Description                                                              | 
+=====================+==========================================================================+
| ID                  | Identificador único da ligação (Unique ID identifier)                    |       
+---------------------+--------------------------------------------------------------------------+
| COD_UF_A            | Código da Unidade da Federação do município A do par de ligação          |  
+                     +                                                                          +
|                     | (Federation Unit Code of Municipality A of the connection pair)          |
+---------------------+--------------------------------------------------------------------------+
| UF_A                | Sigla da Unidade da Federação do município A do par de ligação (Acronym  | 
+                     +                                                                          +
|                     |  of the Federation Unit of municipality A of the connection pair)        |
+---------------------+--------------------------------------------------------------------------+
| CODMUNDV_A          | Código do município A do par de ligação com dígito verificador           |
+                     +                                                                          +
|                     | (Code of municipality A of the connection pair)                          |
+---------------------+--------------------------------------------------------------------------+
| NOMEMUN_A           | Nome do município A do par de ligação (Name of municipality A of the     | 
+                     +                                                                          +
|                     | connection  pair)                                                        |
+---------------------+--------------------------------------------------------------------------+
| COD_UF_B            | Código da Unidade da Federação do município B do par de ligação (Code of | 
+                     +                                                                          +
|                     | the Federative Unit of municipality B of the connection pair)            |
+---------------------+--------------------------------------------------------------------------+
| UF_B                | Sigla da Unidade da Federação do município B do par de ligação (Acronym  |
+                     +                                                                          +
|                     | of the Federation Unit of municipality B of the connection  pair)        |
+---------------------+--------------------------------------------------------------------------+
| CODMUNDV_B          |Código do município B do par de ligação com dígito verificador (Code of   |
+                     +                                                                          +
|                     | the municipality B of the connection pair)                               |
+---------------------+--------------------------------------------------------------------------+
| NOMEMUN_B           | Nome do município B do par de ligação (B municipality name of the        |
+                     +                                                                          +
|                     | connection  pair)                                                        |
+---------------------+--------------------------------------------------------------------------+
| VAR05               | Frequência de saídas de veículos hidroviários no par de ligação          |
+                     +                                                                          +
|                     | (Frequency of  waterway vehicles on the connecting pair)                 |
+---------------------+--------------------------------------------------------------------------+
| VAR06               | Frequência de saídas de veículos rodoviários no par de ligação (Frequency| 
+                     +                                                                          +
|                     | of road vehicles in the connection pair)                                 |
+---------------------+--------------------------------------------------------------------------+
| VAR07               | Frequência total de saídas de veículos no par de ligação (Total frequency| 
+                     +                                                                          +
|                     | of vehicles in the connection pair)                                      |
+---------------------+--------------------------------------------------------------------------+
| VAR08               | Longitude da sede municipal A do par de ligação                          |
+---------------------+--------------------------------------------------------------------------+
| VAR09               | Latitude da sede municipal A do par de ligação                           |
+---------------------+--------------------------------------------------------------------------+
| VAR10               | Longitude da sede municipal B do par de ligação                          |
+---------------------+--------------------------------------------------------------------------+
| VAR11               | Latitude da sede municipal B do par de ligação                           |
+---------------------+--------------------------------------------------------------------------+
| Num_pass            | Number of passengers in the connection pair. Variables that can be       |
+                     +                                                                          +
|                     | created  by  multiplying  the frequency of vehicles per 60.              |
+---------------------+--------------------------------------------------------------------------+


.. note::

  the `Platform for analytical models in epidemiology - PAMEpi <https://pamepi.rondonia.fiocruz.br/en/index_en.html.>`_ offers support in the documentation and collection of this database. More details in [2]_, [3]_ and [4]_.

.. rubric:: References

.. [1] Ligações rodoviárias e hidroviárias: 2016 / IBGE, Coordenação de Geografia. - Rio de Janeiro: IBGE, 2017. 79p. ISBN 978-85-240-4417-5. 
       Retrieved July 03, 2023, from https://biblioteca.ibge.gov.br/visualizacao/livros/liv100602.pdf.
.. [2] Platform for analytical models in epidemiology - PAMEpi. https://pamepi.rondonia.fiocruz.br/en/index_en.html. Accessed: February 25, 2022.
.. [3] GitHub directory - PAMepi/PAMepi-scripts-datalake: v1.0.0 (v1.0.0). Zenodo. . https://doi.org/10.5281/zenodo.6384641. Accessed: February 25, 2022.
.. [4] da Silva, N.B., Valencia, L.I.O., Ferreira, A., Pereira, F.A., de Oliveira, G.L., Oliveira, P.F., Rodrigues, M.S., Ramos, P.I. and Oliveira, J.F., 2022. Brazilian COVID-19 data streaming. arXiv preprint arXiv:2205.05032.

