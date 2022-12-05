Surveillance
=====

Respiratory infections
----------------------

Description
^^^^^^^^^^^

Acute Respiratory Infections are the third cause of mortality worldwide and are usually caused by virus or bacterial agents.

The influenza A(H1N1) pandemic of 2009 highlighted the importance of collecting information about disease severity in a standardized manner and having historical data available for countries to assess current influenza seasons in the context of previous ones [1]_. Thus, since 2009, notification of all hospitalized cases of Severe Acute Respiratory Infection (SARI) is mandatory in Brazil. 

Data on hospitalized SARI cases are inserted and collated in a centralized system, the "Sistema de Informação de Vigilância Epidemiológica da Gripe" (SIVEP-Gripe), which is under governance of the Ministry of Health (MoH).

Following the Covid-19 pandemic, mild Influenza-like illness cases started to be reported on e-SUS Vigilância Epidemiológica (e-SUS-VE), a new national COVID-19 reporting system, also centralized and ran by the MoH. Although currently in use, reporting of mild cases will probably be discontinued as mitigation of the public health emergency caused by Covid-19 goes on.

Both e-SUS-VE and SIVEP-Gripe include suspected and confirmed cases as reported by public health and private services, and case definitions for notification are:

**Hospitalized SARI cases**

A hospitalized patient presenting with the acute onset of fever and cough OR sore throat AND with one of the following: acute respiratory distress, dyspnea, or O2 saturation < 95%. Any patient with the above symptoms and died, regardless of hospitalization.

**Influenza-like illness mild cases**

Any patient presenting with the acute onset of fever (ut to 5 days) and cough OR sore throat.
All notified cases should go under laboratory investigation in order to ascertain the causative agent for confirming or discarding infectious diseases.

Based on the previous description, we collected two databases: the Flu syndrome database (FSdb) and the Severe Acute Respiratory Infection database (SARIdb) to perform studies on AESOP research.

Data access information
^^^^^^^^^^^^^^^^^^^^^^^

The FSdb and SARIdb data are licensed under a Creative Commons Attribution License cc-by (version 4.0) [2]_ and [3]_. Additionally, the databases are publicly available and published by the Ministry of Health of Brazil. Therefore, no approval by an ethics committee is required to use this data, according to Resolutions 466/2012 and 510/2016 (article 1, sections III and V) from the National Health Council (CNS), Brazil.


Methods of data collection
^^^^^^^^^^^^^^^^^^^^^^^^^^

A python code is available on our PAMEpi's GitHub directory to download the FSdb and SARIdb data from the OpenDatasus, see details in [4]_.

Alternatively, FSdb can be downloaded direct from the OpenDatasus links, for the years 2020 to 2022:

	* https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2020,
	* https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2021,
	* https://opendatasus.saude.gov.br/dataset/notificacoes-de-sindrome-gripal-leve-2022.

And SARIdb can be downloaded from OpenDatasus links as shown in https://github.com/cidacslab/AESOP-Data-Documentation/blob/main/Data%20Collection/SRAG.ipynb, for the years 2009 up to 2022.

Data-specific information
^^^^^^^^^^^^^^^^^^^^^^^^^

FSdb is organized according to each federal unit (i.e., state) of the Brazilian federation, while SARSdb files are organized annually (one per year). FSdb is available in .csv format, with a total of 30 variables and a size of around 15 GB in December 2021. In turn, SARSdb, also available in .csv format, contains 161 variables and a size of around 2 GB in December 2021


The FSdb dataset has a total of 30 columns and showed a total of 48,288,827 registries (rows) and a size of 14 GB in the last update of August 19th, 2021. The SRAIdb dataset has a total of 162 columns and showed a total of 1,264,480 registries (rows) and a size of 694 MB in the last update of August 19th, 2021 (informations regarding the files from 2020 up to 2021).

Limitations of the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^

Several cases in the FSdb lack final classification. Every case in FSdb will have a final classification given by the epidemiological surveillance teams of the Secretariat of Health. However, given the number of registered patients, they may not be classified on time (some even closed and not analyzed anymore). To overcome such a difficulty, our team will apply a classification algorithm to give a pre-diagnosis of the cases in FSdb that have no final classification. The algorithm is applied to the information of symptoms that is available in the dataset. 

Every case in SARI will have a final classification given by the epidemiological surveillance teams of the Secretariat of Health. However, given the number of registered patients, they may not be classified on time (some even closed and not analyzed anymore). To overcome such a difficulty, our team will apply a classification algorithm to give a pre-diagnosis of the cases in SRAG that have no final classification. The algorithm is applied to the information of symptoms that is available in the dataset. 

Variable list
^^^^^^^^^^^^^^

Given the extensive number of variables, we refer to https://pamepi.rondonia.fiocruz.br/en/sg_en.html and https://pamepi.rondonia.fiocruz.br/en/srag_en.html for a whole descriptions of the FS and SARI databases [5]and [6]_.  


Arboviruses infections 
----------------------

Description
^^^^^^^^^^^
Arbovirus (arthropod-borne virus) infection is an infection caused by a viral spread to humans (and/or other vertebrates) through the bite of a blood-feeding arthropods (eg. flies, mosquitoes, ticks, etc). There are more than 250 species of arbovirus, including dengue, Zika, chikungunya, West Nile, Yellow fever, and others.  An Arbovirus catalog is described `here <https://wwwn.cdc.gov/Arbocat/Default.aspx>`_.

For the purposes of the AESOP project, we collected data of suspected Dengue, Zika and Chikungunya infections that were reported and are available in the `Notifiable Diseases Information System (SINAN) <https://portalsinan.saude.gov.br>`_. The notification of every suspected case of these 3 diseases is mandatory, and case definition are as follows:

**Dengue:** 

Suspect case:
Any patient residing in (or having traveled to in the previous 14 days), an area with dengue or Aedes aegypti occurrence, and who presents with acute onset of fever (lasting up to 7 days) and 2 or more of the following symptoms: nausea/vomiting, rash, myalgia/arthralgia, headache, retro-orbital pain, petechiae, positive tourniquete test, leukopenia

**Chikungunya**

Suspect case:
Any patient presenting with sudden onset of high fever (>38.5°C) and acute onset of arthralgia or severe arthritis not explained by other conditions, residing in (or having visited in the previous 14 days) areas with chikungunya transmission, or who has an epidemilogic link to a confirmed imported case

**Zika**

Suspect case:
Any patient presenting with pruritic maculopapular rash and one of the following: fever, conjunctival hyperaemia/non-purulent conjunctivitis, arthralgia/polyarthralgia, Periarticular edema.

In each disease, a patient will be assigned as a confirmed case of dengue, Zika or chinkungunya infection when a laboratory test (PCR, serology, virus isolation) is confirmed OR, when laboratory analysis is not possible, when the case is compatible with clinical presentation AND with epidemiologic link to a confirmed case AND for which no other diagnosis was confirmed.

.. note::

  the `Platform for analytical models in epidemiology - PAMEpi <https://pamepi.rondonia.fiocruz.br/en/index_en.html.>`_ offers support in the documentation and collection of this database. More details in [4]_, [5]_ and [6]_.

.. rubric:: References

.. [1] PAHO. Operational Guidelines for Sentinel Severe Acute Respiratory Infection (SARI) Surveillance. September 2014. https://www.paho.org/hq/dmdocuments/2015/2015-cha-operational-guidelines-sentinel-sari.pdf

.. [2] Ministério da Saúde. Open Datasus. Notificações de Síndrome Gripal. Retrieved 08 25, 2021, from https://opendatasus.saude.gov.br/dataset/casos-nacionais

.. [3] Ministério da Saúde. Open Datasus. Banco de dados SRAG. Retrieved 04 25, 2021, from https://opendatasus.saude.gov.br/dataset/bd-srag-2021/resource/42bd5e0e-d61a-4359-942e-ebc83391a137, https://opendatasus.saude.gov.br/dataset/bd-srag-2021

.. [4] Platform For Analytical Modelis in Epidemiology. (2022). PAMepi/PAMepi-scripts-datalake: v1.0.0 (v1.0.0). GitHub directory: https://github.com/PAMepi/PAMepi_scripts_datalake.git. Zenodo. . https://doi.org/10.5281/zenodo.6384641. Accessed: February 25, 2022.

.. [5] Platform for analytical models in epidemiology - PAMEpi. https://pamepi.rondonia.fiocruz.br/en/index_en.html. Accessed: February 25, 2022.

.. [6] da Silva, N.B., Valencia, L.I.O., Ferreira, A., Pereira, F.A., de Oliveira, G.L., Oliveira, P.F., Rodrigues, M.S., Ramos, P.I. and Oliveira, J.F., 2022. Brazilian COVID-19 data streaming. arXiv preprint arXiv:2205.05032.

