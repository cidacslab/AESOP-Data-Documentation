# -*- coding: utf-8 -*-
#%additional_python_modules s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/python_utils/teste.py
#%extra_py_files s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/python_utils/util_custom.py
#%additional_python_modules s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epiweeks-2.3.0-py3-none-any.whl


import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


from util_custom import *
from pyspark.sql import functions as F
from pyspark.sql.types import *
import os
from datetime import datetime, timedelta
from pyspark.sql.window import Window
from epiweeks import Week

import boto3
from botocore.exceptions import ClientError
import pandas as pd

arquivo = pd.read_csv(nome_parquet, header=None)
content = arquivo.iloc[0, 0]

def create_folder_in_specific_location(bucket_name, full_folder_path):
    # Adiciona uma barra ao final do caminho da pasta, se não houver
    if not full_folder_path.endswith('/'):
        full_folder_path += '/'
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    
    # Verifica se a pasta já existe
    objs = list(bucket.objects.filter(Prefix=full_folder_path))
    if any(obj.key == full_folder_path for obj in objs):
        print(f"A pasta '{full_folder_path}' já existe no bucket '{bucket_name}'.")
    else:
        # Tenta criar a pasta (objeto S3 com chave terminando em '/')
        try:
            s3.Object(bucket_name, full_folder_path).put(Body=b'')
            print(f"Pasta '{full_folder_path}' criada com sucesso no bucket '{bucket_name}'.")
        except ClientError as e:
            print(f"Erro ao criar a pasta: {e}")


def list_all_files_in_folders_s3(bucket_name, prefix):
    """
    Lista todos os arquivos dentro de todas as subpastas de um prefixo específico em um bucket S3.

    :param bucket_name: Nome do bucket S3.
    :param prefix: Prefixo dentro do bucket onde as subpastas estão localizadas.
    :return: Uma lista de nomes de arquivos dentro de todas as subpastas sob o prefixo especificado.
    """
    s3 = boto3.client('s3')
    all_files = []

    # Garante que o prefixo termine com uma barra, se já não terminar.
    if not prefix.endswith('/'):
        prefix += '/'

    # Lista todas as 'subpastas' dentro do prefixo.
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')

    subfolders = []
    if 'CommonPrefixes' in response:
        for folder in response['CommonPrefixes']:
            subfolders.append(folder['Prefix'])

    # Para cada subpasta, lista todos os arquivos dentro dela.
    for folder_name in subfolders:
        resp = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
        if 'Contents' in resp:
            for file in resp['Contents']:
                # Adiciona o nome do arquivo à lista
                all_files.append(file['Key'])
    data_max = sorted(all_files)[-1][-12:-4]
    return data_max


# Exemplo de uso
bucket_name = 'fiocruz-datalake-bucket'


# #### leitura banco HPC

aesop_2017_2024 = spark.read.parquet(f"{legada_path}/{content}_AESOP.parquet/")

max_ano = aesop_2017_2024.agg(F.max("ano")).collect()[0][0]
semana_folder = aesop_2017_2024.filter(F.col("ano") == max_ano).agg(F.max("epiweek")).collect()[0][0]
#semana_folder

aesop_report_folder  = "standard/reports/report_dqi/"

caminho_pasta = aesop_report_folder+"semana_"+str(semana_folder)+"_"+str(max_ano)
caminho_pasta
create_folder_in_specific_location(bucket_name,caminho_pasta)


# #### leitura banco raw parquet

df = spark.read.parquet(f'{escrita_aesop_to_parquet}/aesop_dados_{content}.parquet/')

df = df.filter((F.col("FX_ETARIA")).isNotNull())
df_v2 = df.select("ANO","SEMANA","SG_UF","CO_MUNICIPIO_IBGE","SEXO","FX_ETARIA","CIDCIAP","QT","Data_folder")

# #### converter cid_ciap


df_v3 = df_v2\
.withColumn("Tipo_CIDCIAP", F.substring_index(df_v2.CIDCIAP, '(', 1))\
.withColumn("Codigo_CIDCIAP", F.substring_index(df_v2.CIDCIAP, '(', -1))

df_v3 = df_v3.withColumn('Codigo_CIDCIAP', F.concat(F.lit("("), F.col('Codigo_CIDCIAP')))

# OBS: max semana folder passa da epiweek

sisab_diff = df_v3.groupBy("ANO", "SEMANA", "SG_UF", "CO_MUNICIPIO_IBGE", "Data_folder").agg(F.sum("QT").alias("qt_total")).cache()


# #### gerar dados report dqi

ibge_munic = spark.read.csv(ibge_munic_path, header=True, sep=';').drop('_c0')


#semanas_epis = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epiweek_ibge2017_20241231.parquet/")
#semanas_epis = spark.read.csv(epiweek_ibge2017_2023_PATH,header=True)

semanas_epis = spark.read.option("mergeSchema", "true").parquet(epiweek_ibge2017_2023_PATH)
semanas_epis = semanas_epis.withColumnRenamed("semana_ibge", "SEMANA")
semanas_epis = semanas_epis.withColumnRenamed("ano_ibge", "ANO")
semanas_epis = semanas_epis.withColumnRenamed("co_ibge", "CO_MUNICIPIO_IBGE")


#dado com todos os dias de 2017 a 2024 com as semanas epidemio respectivas
#epi_week_python = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/dados_epidemiologicos_2017_2024.parquet").filter(F.col("ano_epidemiologic") <= 2024)
epi_week_python = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/dados_epidemiologicos_2017_2025.parquet")

#dado por semana, contendo o ultimo dia de cadas semama epidemio
#last_first_day_epiweek = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epi_week_first_last_day_2017a2024.parquet/")
last_first_day_epiweek = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epi_week_first_last_day_2017a2025.parquet/")

epi_week = epi_week_python.join(last_first_day_epiweek,['semana','ano'],'inner')

epi_week_dt_folder = epi_week.withColumnRenamed("dates", "Data_folder").select("Data_folder","ultimo_dia_week_epidemio")



sisab_diff = sisab_diff.join(epi_week_dt_folder,['Data_folder'],'inner')


sisab_diff = sisab_diff.withColumnRenamed("ultimo_dia_week_epidemio", "dt_folder")

last_first_day_epiweek_dt_encounter = last_first_day_epiweek.withColumnRenamed("ultimo_dia_week_epidemio", "dt_encounter").drop("primeiro_dia_week_epidemio") #cria o dt enconter, último dia da semana epi da semana de atendimento
last_first_day_epiweek_dt_encounter = last_first_day_epiweek_dt_encounter.withColumnRenamed("semana_epidemiologica", "SEMANA")
last_first_day_epiweek_dt_encounter = last_first_day_epiweek_dt_encounter.withColumnRenamed("ano_epidemiologic", "ANO")

sisab_diff = sisab_diff.join(last_first_day_epiweek_dt_encounter,['SEMANA','ANO'],'inner')


#diferença em dias de dt_folder para dt_encounter
sisab_diff = sisab_diff.withColumn("date_diff", F.datediff("dt_folder","dt_encounter") ) 

#diff de semanas entre atendimento estimado e data do envio
sisab_diff = sisab_diff.withColumn("week_diff", F.col("date_diff") / 7 )  


semana_filter = semana_folder-7
ano_filter = max_ano
if semana_filter < 1:
    ano_filter = ano_filter-1
    semana_filter = 52+semana_filter
    
print(semana_filter)
print(ano_filter)

filter_date = sisab_diff.filter(F.col('ANO') == ano_filter)\
.filter(F.col('SEMANA') == semana_filter)\
.select(F.max(F.col('dt_encounter')) ).collect()[0][0]
print(filter_date) 

ano_max = sisab_diff.agg(F.max("ANO").alias("max_ano"))
ano_max = ano_max.collect()[0]["max_ano"]
print(semana_folder)
print(ano_max)

#week_filter = "2023-01-07"

# Step 1: Filter based on `dt_folder`
completude = sisab_diff.filter(sisab_diff['dt_encounter'] >= filter_date)

# Step 2: Select specific columns and remove others
#tempestividade = tempestividade.drop('Data_folder', 'ANO', 'SEMANA', 'SG_UF')
completude = completude\
.drop('Data_folder', 'ANO', 'SEMANA', 'SG_UF', 'first_day_of_year', 'date_diff')\
.withColumnRenamed('CO_MUNICIPIO_IBGE', 'co_ibge')

# complete command
ibge = completude.select('co_ibge').distinct()
dt_encounter = completude.select('dt_encounter').distinct()
ibge_dtencounter = ibge.crossJoin(dt_encounter)
# complete join back
completude = ibge_dtencounter.join(completude, ['co_ibge', 'dt_encounter'], 'left')

# count 
completude = completude.groupBy('co_ibge', 'dt_encounter')\
.agg(F.sum('qt_total').alias('n'))\
.na.fill({'n': 0})


# slider
ws = Window.partitionBy("co_ibge").orderBy("dt_encounter").rowsBetween(-7, Window.currentRow)

# UDF for epiweek and epiyear
epiweekUDF = F.udf(lambda z:  Week.fromdate(z).week, IntegerType())
epiyearUDF = F.udf(lambda z:  Week.fromdate(z).year, IntegerType())

# slider as window function
completude_missings = completude\
.withColumn("empty", F.when(F.col('n')==0, 1).otherwise(0))\
.withColumn("window_size", F.count("*").over(ws))\
.withColumn("start", F.min("dt_encounter").over(ws))\
.withColumn("end", F.max("dt_encounter").over(ws))\
.withColumn("no_missings", F.sum("empty").over(ws))\
.filter(F.col('window_size')==8)\
.withColumn("epi_week", epiweekUDF(F.col('dt_encounter')))\
.withColumn("epi_year", epiyearUDF(F.col('dt_encounter')))\
.drop('window_size', 'empty', 'n', 'dt_encounter')\
.filter(F.col('epi_week')==semana_folder)

# add missing cities 
completude_miss_ibge = ibge_munic.join(completude_missings, ['co_ibge'], 'full')

# calculate percentages
# correcao da semana e ano vazias por não estarem esses municipios e consequentemente as semanas e ano 
comp_percentage = completude_miss_ibge.na.fill({'no_missings': 8,'epi_week':semana_folder,'epi_year':ano_max})\
.withColumn('perc_missing',  F.col('no_missings')/8*100)\
.withColumn('perc_completude',  100-F.col('perc_missing'))



# #### tempestividade 

# Step 1: Filter based on `dt_folder`
tempestividade = sisab_diff.filter( F.col("dt_folder")  >= filter_date)

# Step 2:dropa algumas colunas
tempestividade = tempestividade.drop('Data_folder', 'ANO', 'SEMANA', 'SG_UF')

# faz o complete dos dados levando em conta todas as possibilidades de CO_MUNICIPIO_IBGE x dt_folder
co_ibge_df = tempestividade.select("CO_MUNICIPIO_IBGE").distinct()
dt_folder_df = tempestividade.select("dt_folder").distinct()
all_combinations_df = co_ibge_df.crossJoin(dt_folder_df)

# faz o join para o lado completo criando anteriormente
tempestividade2 = all_combinations_df.join(tempestividade, ["CO_MUNICIPIO_IBGE", "dt_folder"], "left_outer")

#conta os atendimento para as 8 semanas de dados
tempestividade3_p1 = tempestividade2.groupBy("CO_MUNICIPIO_IBGE").agg(F.sum("qt_total").alias("total_atd_folder"))

#faz categorias  a partir da diff em semanas entre atendimento e envio para as ultimas 8 semanas. se ate 2 semanas de diff,  0_2weeks , se maior que duas semanas, 3+weeks,soma-se o total de atendimento para cada categoria criada.
tempestividade3_p2 = tempestividade2.withColumn("diff", F.when(  F.col("week_diff") <= 2, "0_2weeks").otherwise(
                                                        F.when(   F.col("week_diff") > 2, "3+weeks"  )    ) ) .groupBy("CO_MUNICIPIO_IBGE","diff").agg( F.sum("qt_total").alias("qt_diff") )

#junta o atendimento total das 8 semanas com os atendimentos das 8 semanas categorizado entre 0_2weeks e   3+weeks
tempestividade3 = tempestividade3_p1.join(tempestividade3_p2 , ['CO_MUNICIPIO_IBGE'])
tempestividade3 = tempestividade3.withColumn("diff_percent", F.col("qt_diff") / F.col("total_atd_folder") * 100)
tempestividade3 = tempestividade3.withColumn("diff_percent2",F.round("diff_percent",5))

#pivota os dados para as variáveis de porcetagem 0_2weeks e 3+weeks irem para colunas
tempestividade4  = tempestividade3.groupBy("CO_MUNICIPIO_IBGE").pivot("diff").agg(F.first("diff_percent2"))
tempestividade5 = tempestividade4.withColumnRenamed("0_2weeks","diff_2w")
tempestividade5 = tempestividade5.withColumnRenamed("3+weeks","diff_3w")
tempestividade5 = tempestividade5.withColumn("co_ibge",F.col("CO_MUNICIPIO_IBGE").cast(StringType() ) ).drop("CO_MUNICIPIO_IBGE","diff_2w_new","diff_3w_new","null").cache()

#agrupar os dados de "ANO","SEMANA","SG_UF","CO_MUNICIPIO_IBGE" somando o qt_total
df_agg = sisab_diff.groupBy("ANO","SEMANA","SG_UF","CO_MUNICIPIO_IBGE").agg(F.sum("qt_total").alias("qt_total")) 

epi_week_atend_2week = epi_week.withColumnRenamed('semana_epidemiologica', 'SEMANA')
epi_week_atend_2week = epi_week_atend_2week.withColumnRenamed('ano_epidemiologic', 'ANO')
epi_week_atend_2week = epi_week_atend_2week.select("SEMANA","ANO").dropDuplicates()


epi_week_atend_2week_v2 = epi_week_atend_2week.filter(
    (F.col("ANO").between(2017, ano_max-1)) |
    ((F.col("ANO") == ano_max) & (F.col("SEMANA") <= semana_folder))
)

co_ibge_unicos = semanas_epis.select("CO_MUNICIPIO_IBGE").distinct()

epi_week_atend_2week_v3 = epi_week_atend_2week_v2.crossJoin(co_ibge_unicos)


#junta com os dados das semanas epidemiologicas completas, filtrando em seguida para dados ate 2024 e que a semana sejam somente as duas últimas, ou seja menor que a semana folder(semana atual) e maior que a semana folder - 1, ex: semana 47 seria de 46 a 47
df_agg_v2 = epi_week_atend_2week_v3.join(df_agg , ["ANO","SEMANA","CO_MUNICIPIO_IBGE"] , 'left')

df_agg_v3 = df_agg_v2.filter(F.col("ANO") == 2025)

df_agg_v4 = df_agg_v3.filter(F.col("SEMANA") <= semana_folder).filter(F.col("SEMANA") >= semana_folder-1)  # capturar somente ate a semana atual , e somente maiores que a semana atual - 1 

#para criar a variável sum_miss que tem 3 categorias, 0(com atendimentos nas 2 semanas) , 1 (com atendimento em somente 1 das duas semanas ) e 2 (sem atendimetnos nas duas semanas)
windowSpec = Window.partitionBy("CO_MUNICIPIO_IBGE")

df_agg_v5 = df_agg_v4.withColumn("count_empty", F.sum(F.when(F.col("qt_total").isNull(), 1).otherwise(0)).over(windowSpec))
df_agg_v6 = df_agg_v5.select("CO_MUNICIPIO_IBGE","SEMANA","ANO","count_empty").groupBy("CO_MUNICIPIO_IBGE").agg(F.first("count_empty").alias("sum_miss"))
df_agg_v7 = df_agg_v6.withColumn("co_ibge",F.col("CO_MUNICIPIO_IBGE").cast(IntegerType()).cast(StringType()) ).drop("CO_MUNICIPIO_IBGE")

dqi = df_agg_v7.join(tempestividade5,['co_ibge'],'left')

last_first_day_epiweek_consistencia = last_first_day_epiweek.withColumnRenamed("semana", "epiweek")
last_first_day_epiweek_consistencia = last_first_day_epiweek_consistencia.withColumnRenamed("ano", "ano")

aesop_2017_2024_grouped = aesop_2017_2024.groupby("co_ibge","epiweek","ano").agg(F.sum("atend_totais").alias("atend_totais")).cache()

aps =  aesop_2017_2024_grouped.join(last_first_day_epiweek_consistencia,['epiweek','ano'],'left').drop("primeiro_dia_week_epidemio")


data_max = aps.select(F.max("ultimo_dia_week_epidemio")).first()[0]
data_max


data_limite_final = data_max - timedelta(weeks=12)
data_limite_final


data_limite_inicial = data_limite_final - timedelta(weeks=12)
data_limite_inicial


f_inicial = F.col("ultimo_dia_week_epidemio") >= data_limite_inicial
f_final = F.col("ultimo_dia_week_epidemio") < data_limite_final

aps_periodo = aps.filter(f_inicial & f_final)

media_desvio = aps_periodo.groupBy("co_ibge").agg(F.avg("atend_totais").alias("media"),
                                                           F.stddev("atend_totais").alias("sd"))

media_desvio = media_desvio.withColumn("upper_sd",F.col("media") + (2 * F.col("sd") ))
media_desvio = media_desvio.withColumn("lower_sd",F.col("media") - (2 * F.col("sd") ))


aps_ultima_semana = aps.filter(data_max == F.col("ultimo_dia_week_epidemio") )
aps_ultima_semana_v2 = aps_ultima_semana.join(media_desvio,['co_ibge'],'left')


aps_ultima_semana_v2 = aps_ultima_semana_v2.withColumn("consistencia", F.when(F.col("atend_totais") >= F.col("lower_sd"),"valido"  ).otherwise(F.lit("invalido")) )
aps_ultima_semana_v3 = aps_ultima_semana_v2.select("co_ibge","consistencia","media","lower_sd","upper_sd","sd")



dqi_v2 = dqi.join(comp_percentage,['co_ibge'],'left')
dqi_v3 = dqi_v2.join(aps_ultima_semana_v3,['co_ibge'],'left')

dqi_v3 = dqi_v3.withColumn("tempestividade",F.when(F.col("diff_2w") >=  80,  0).otherwise(1)  )
dqi_v3 = dqi_v3.withColumn("completude",F.when(F.col("perc_completude") >=  100, 0).otherwise(1)  )

cond1 = F.col("completude") == 0
cond2 = F.col("tempestividade") == 0
cond3 = F.col("consistencia") == "valido"
#cond3 = F.col("sum_miss") == 0

dqi_v3 = dqi_v3.withColumn("dqi",F.when( cond1 & cond2 & cond3 , "Apto").otherwise("Não Apto")  ) # condição do sum_miss foi removida e diff_2w saiu de 75 para 80, perc_completude de 80 para 100 em 10/06/2024
#em 01/08/2024  foi adicionado a metrica consistencia, para ser apto precisa ser valido


dqi_v4 = dqi_v3.select("uf", "co_ibge", "municipio", "epi_week", "epi_year", "perc_missing", "perc_completude", "diff_2w", "diff_3w","media","lower_sd","upper_sd","sd", "sum_miss", "completude", "tempestividade","consistencia", "dqi")
dqi_v4 = dqi_v4.na.fill({'diff_2w': 0, 'diff_3w': 0}).cache()


path_salvar = "s3://fiocruz-datalake-bucket/"+caminho_pasta


#path_salvar_dqi = aesop_dqi_report_folder+'semana_'+str(semana_folder)+"/dqi.csv"
total_linhas = dqi_v4.count()

# Contagem de linhas sem valores nulos
linhas_sem_nulos = dqi_v4.na.drop().count()

if total_linhas != linhas_sem_nulos:
    print("O DataFrame contém valores nulos.")
else:
    print("O DataFrame não contém valores nulos.")

dqi_v4.toPandas().to_csv(path_salvar+"/dqi.csv",index=False)
path_salvar


#get_ipython().run_line_magic('stop_session', '')

# Finalize o trabalho Glue e pare a sessao Spark
job.commit()
spark.stop()