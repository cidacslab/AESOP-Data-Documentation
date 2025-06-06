# -*- coding: utf-8 -*-
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
import pandas as pd
#from epiweeks import Week

#df = spark.read.parquet(aesop_parquet_path+get_parquet_file_name())
#aesop_parquet_path+get_parquet_file_name()



arquivo = pd.read_csv(nome_parquet, header=None)
content = arquivo.iloc[0, 0]

df = spark.read.parquet(f'{escrita_aesop_to_parquet}/aesop_dados_{content}.parquet/')
#print(f'{escrita_aesop_to_parquet}/{content}')

#df.count()  #1165697215

n_semana_max = get_max_semana_from_aesop_dados(df, 'ano', 'semana')
#n_semana_max

res = df.groupBy("ano").agg(F.max("semana").alias("max_semana"),F.min("semana").alias("min_semana"))

#res.orderBy("ano").show(100)

# Define a UDF to apply the date calculation

def return_day(week, year):
    # Calculate the timestamp for December 31 of the previous year
    prev_year = year - 1
    timestamp_dec_31 = datetime(prev_year, 12, 31)
    # Calculate the target date by adding (week * 7) days and rest 3 days
    target_date = timestamp_dec_31 + timedelta(days=week * 7 - 3)
    return target_date

# Register the UDF
return_day_udf = F.udf(return_day, DateType())

# Apply the UDF to the DataFrame
df = df.withColumn("DATE", return_day_udf(df["SEMANA"], df["ANO"]))

df_v2 = df\
.filter(F.col("ANO") >= 2017)\
.filter(F.col("FX_ETARIA").isNotNull())

#criar variável para o tipo do codigo, pode ser CID/CIAP/AB , usa-se split para quebrar a variável de entrada pelo primeiro paratese 
df_v2 = df_v2.withColumn("tipo_codigo", F.split(F.col("CIDCIAP"), "\\(").getItem(0))
#remover ponto dos cids/ciap/ab
df_v2 = df_v2.withColumn("CIDCIAP_v2", F.regexp_replace(F.col("CIDCIAP"), "\\.", ""))

# extrair codigo de dentro dos parenteses
# exemplo CID(Z00) -> Z00
regex_pattern = r'\(([^)]+)\)'
df_v2 = df_v2.withColumn("CIDCIAP_v3", F.trim(F.regexp_extract(F.col("CIDCIAP_v2"), regex_pattern, 1)))

# quem tiver 4 digitos vai ficar somente com 3 digitos para ser usado na criação da variável ivas posteriomente
# ex  L028 -> L02
condition = (F.length(F.col('CIDCIAP_v3')) == 4) #esse jeito não serve para a nova var de arbovirose
df_v2 = df_v2.withColumn(
    'Codigo_CIDCIAP_3digits',F.when(condition, F.expr("substring(CIDCIAP_v3, 1, length(CIDCIAP_v3)-1)"))
    .otherwise(F.col('CIDCIAP_v3'))
)

# concatena tipo + codigo 
df_v2 = df_v2.withColumn("tipo_codigo_3digits", F.concat_ws("", F.col("tipo_codigo"), F.col("Codigo_CIDCIAP_3digits") ) )
df_v2 = df_v2.withColumn("tipo_codigo_full_digits", F.concat_ws("", F.col("tipo_codigo"), F.col("CIDCIAP_v3") ) )

df_v3 = df_v2.drop("CIDCIAP") # tipo_codigo é o tipo do código pode ser CID/CIAP/AB

# As IVAS são infecções virais das vias aéreas superiores
codigos_ivas_numero = ['CIAPA03','CIAPR01','CIAPR02','CIAPR03','CIAPR04','CIAPR05','CIAPR07','CIAPR08','CIAPR21','CIAPR23','CIAPR25','CIAPR29','CIAPR71','CIAPR74','CIAPR75',
                       'CIAPR76','CIAPR77','CIAPR78','CIAPR80','CIAPR81','CIAPR83','CIAPR99','CIDJ00','CIDJ01','CIDJ02','CIDJ03','CIDJ04','CIDJ06','CIDJ09','CIDJ10',
                       'CIDJ11','CIDJ12','CIDJ13','CIDJ14','CIDJ15','CIDJ16','CIDJ17','CIDJ18','CIDJ20','CIDJ21','CIDJ22','CIDJ80','CIDR05','CIDR06','CIDR07','CIDR43',
                       'CIDR50','CIDU07','CIDB34','CIDB97']
# cria nova coluna com valores zerados em CIDS/CIAPS fora do ivas
df_v3 = df_v3.withColumn("atend_ivas",F.when( (F.col("tipo_codigo_3digits").isin(codigos_ivas_numero) ), F.col("QT")).otherwise(0))
# zera valores para ivas_exclusao
codigos_ivas_exclusao = ['CIDR072']
df_v4 = df_v3.withColumn("atend_ivas_v2",F.when( (F.col("tipo_codigo_full_digits").isin(codigos_ivas_exclusao) ), 0).otherwise(F.col("atend_ivas")))

# As arboviroses são um grupo de doenças causadas por arbovírus
codigos_arbov_numero = [
    'CIAPA77', 'CIDA90', 'CIDA91', 'CIDA92', 'CIDA920','CIDA925', 'CIDA928', 'CIDA929', 'CIDA99', 'CIDA98',
    'CIDA97','CIDA93','CIDA972','CIDA979','CIDA988','ABABP019','CIDA930' #CIDA930 adicionado em 01/07/2024
]
# Dicionário_CódigosARBOV update em 22/12/2023
df_v4 = df_v4.withColumn("atend_arbov",F.when( (F.col("tipo_codigo_full_digits").isin(codigos_arbov_numero) ), F.col("QT")).otherwise(0))#.checkpoint()

#df_v4.agg(F.sum("atend_arbov")).collect()[0][0] #12191215

#df_v4.filter(F.col("atend_arbov") >= 1).groupBy("tipo_codigo_full_digits").agg(F.sum("QT").alias("QT") ).show(1000,False)

df_v5 = df_v4\
.withColumnRenamed('DATE', 'calendar')\
.withColumnRenamed('SEMANA', 'epiweek')\
.withColumnRenamed('ANO', 'epi_year')

# cria base municipal
df_v6 = df_v5.groupBy("CO_MUNICIPIO_IBGE",'epi_year',"epiweek")\
.agg(
    F.sum("QT").alias("atend_totais"),
    F.sum("atend_ivas_v2").alias("atend_ivas"),
    F.last("calendar").alias('calendar'), 
    F.sum("atend_arbov").alias("atend_arbov")
)

df_v7 = df_v6.withColumnRenamed("epi_year","ANO").withColumnRenamed("epiweek","SEMANA")
df_v7 = df_v7.withColumn('Ano_Epiweek', F.substring('calendar', 1,4))
df_v7 = df_v7.withColumn('Mes_Epiweek', F.substring('calendar', 6,2))

AB_2017_2023_AGGREGATE_FINAL = spark.read.parquet(AB_2017_2023_AGGREGATE_FINAL_PATH)
AB_2017_2023_AGGREGATE_FINAL = AB_2017_2023_AGGREGATE_FINAL.withColumnRenamed("Ano","Ano_AB")\
                                                           .withColumnRenamed("Mes","Mes_AB")
AB_2017_2023_AGGREGATE_FINAL = AB_2017_2023_AGGREGATE_FINAL.drop('Unnamed: 0')
AB_2017_2023_AGGREGATE_FINAL = AB_2017_2023_AGGREGATE_FINAL.withColumn('MERGE_COUNT_AB',F.lit(1))

AB_2017_2023_AGGREGATE_FINAL = AB_2017_2023_AGGREGATE_FINAL\
.withColumn("Mes_AB", 
            F.when(F.length(AB_2017_2023_AGGREGATE_FINAL.Mes_AB) < 2,
                   F.concat(F.lit('0'), F.col('Mes_AB'))).otherwise(AB_2017_2023_AGGREGATE_FINAL.Mes_AB)
           )

df_v8 = df_v7.join(AB_2017_2023_AGGREGATE_FINAL, 
   on=[
     df_v7.CO_MUNICIPIO_IBGE == AB_2017_2023_AGGREGATE_FINAL.Ibge, 
     df_v7.Mes_Epiweek == AB_2017_2023_AGGREGATE_FINAL.Mes_AB,
     df_v7.Ano_Epiweek == AB_2017_2023_AGGREGATE_FINAL.Ano_AB 
   ], how='left')

df_v9 = df_v8.withColumnRenamed("calendar","Date_epiweek")
df_v9 = df_v9.select(
    "CO_MUNICIPIO_IBGE",
    "Date_epiweek",
    "SEMANA",
    "Mes_Epiweek",
    "ANO",
    "atend_totais",
    "atend_ivas",
    "atend_arbov",
    "PC_COBERTURA_SF",
    "PC_COBERTURA_AB"
)

epiweek_ibge2017_2023 = spark.read.parquet(epiweek_ibge2017_2023_PATH)
epiweek_ibge2017_2023.printSchema()

#epiweek_ibge2017_2023 = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epiweek_ibge2017_20241231.parquet")

schema_epiweek = StructType([
    StructField("semana", StringType(), True),
    StructField("ano", StringType(), True),
    StructField("uf", StringType(), True),
    StructField("co_ibge", StringType(), True),
    StructField("municipio", StringType(), True),
    StructField("pop_2010", StringType(), True),
    StructField("porte", StringType(), True)
])


#epiweek_ibge2017_2023 = spark.read.schema(schema_epiweek).parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epiweek_ibge2017_20241231.parquet")

#epiweek_ibge2017_2023.count()

epiweek_ibge2017_2023.printSchema()

#epiweek_ibge2017_2023.select("co_ibge").distinct().count()

#epiweek_ibge2017_2023 = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/epiweek_ibge2017_20241231.parquet/")
# renomear
epiweek_ibge2017_2023 = epiweek_ibge2017_2023\
.withColumnRenamed("uf","uf_ibge")\
.withColumnRenamed("ano","ano_ibge")\
.withColumnRenamed("semana_int","semana_ibge")

# cast
epiweek_ibge2017_2023 = epiweek_ibge2017_2023\
.withColumn("semana_ibge_int",F.col("semana_ibge").cast(ShortType()))\
.withColumn("ano_ibge",F.col("ano_ibge").cast(ShortType()))\
.withColumn("co_ibge",F.col("co_ibge").cast(IntegerType()))

# anos com 52 semanas
filtro_anos_anteriores = F.col("ano_ibge").isin([2017,2018,2019,2020,2022,2023,2024]) # esses ano não é verificado se tem semana 53. verificar de fato no script de validar e emitir alerta quando surgir

# o ano de 2021 teve 53 semanas
filtro_2021_ano = F.col("ano_ibge") == 2021
filtro_2021_week = F.col("semana_ibge_int") <= 52
# filtrando ano atual
filtro_atual_ano = F.col("ano_ibge") == 2025
filtro_atual_week = F.col("semana_ibge_int") <= n_semana_max
# aplicando filtros
epiweek_ibge2017_2023_filtro = epiweek_ibge2017_2023.filter(filtro_anos_anteriores  | (filtro_2021_ano & filtro_2021_week) | (filtro_atual_ano & filtro_atual_week))

df_v10 = epiweek_ibge2017_2023_filtro.join(df_v9, 
   on=[
     epiweek_ibge2017_2023_filtro.co_ibge == df_v9.CO_MUNICIPIO_IBGE, 
     epiweek_ibge2017_2023_filtro.ano_ibge == df_v9.ANO, 
     epiweek_ibge2017_2023_filtro.semana_ibge_int == df_v9.SEMANA
   ], how='left')

df_v10 = df_v10.withColumn("PC_COBERTURA_SF", F.regexp_replace(F.col("PC_COBERTURA_SF"), ",", ".").cast("double"))
df_v10 = df_v10.withColumn("PC_COBERTURA_AB", F.regexp_replace(F.col("PC_COBERTURA_AB"), ",", ".").cast("double"))

colunas = ['atend_totais', 'atend_ivas', 'atend_arbov', 'PC_COBERTURA_SF', 'PC_COBERTURA_AB']

# Preencher as colunas com zero
fill_values = {coluna: 0 for coluna in colunas}
#fill_values

df_v11 = df_v10.fillna(fill_values)

REGIAO_IMEDIATA_BRASIL = spark.read.parquet(REGIAO_IMEDIATA_BRASIL_PATH)
REGIAO_IMEDIATA_BRASIL = REGIAO_IMEDIATA_BRASIL.withColumn("CD_GEOCODI_6", F.substring(F.col("CD_GEOCODI"),1,6))

df_v12 = df_v11.join(REGIAO_IMEDIATA_BRASIL, F.col("co_ibge") == F.col("CD_GEOCODI_6"),'left').drop("ANO")

df_v12 = df_v12\
.withColumnRenamed("uf_ibge","UF")\
.withColumnRenamed("ano_ibge","ano") \
.withColumnRenamed("semana_ibge","epiweek")\
.drop("Mes_Epiweek",'UF','CD_GEOCODI')

df_v12 = df_v12.withColumnRenamed("PC_COBERTURA_SF","pc_cobertura_sf")
df_v12 = df_v12.withColumnRenamed("PC_COBERTURA_AB","pc_cobertura_ab")

df_v12 = df_v12.withColumn("epiweek",F.col("epiweek").cast(IntegerType()))

df_legada = df_v12.select(
    "municipio",
    'co_ibge',
    "ano",
    "epiweek",
    "atend_totais",
    "atend_ivas",
    "atend_arbov",
    "pc_cobertura_sf",
    "pc_cobertura_ab",
    "cod_rgimediata",
    "nome_rgi",
    "cod_rgint",
    "nome_rgint"
) 

#diretorio = aesop_hpc_path+"2017_"+str(get_latest_date_aesop())+"_AESOP.parquet"
#diretorio

df_legada.write.parquet(f"{legada_path}/{content}_AESOP.parquet")

single_file = spark.read.parquet(f"{legada_path}/{content}_AESOP.parquet")

single_file.count() #2183440

single_file\
.repartition(1)\
.write.format("parquet").mode("error")\
.save(f"{single_file_path}/{content}_AESOP.parquet", mode = 'overwrite')

#renomear_arquivo_unico(diretorio, "base_aps_atual.parquet")

#%stop_session
# Finalize o trabalho Glue e pare a sessao Spark
job.commit()
spark.stop()
