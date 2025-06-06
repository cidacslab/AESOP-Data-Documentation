# Salve este script como s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/python_utils/meu_script.py
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
import pandas as pd
print("bases anuais {}".format(aesop_csv_anual_path))
print("bases anuais abp {}".format(aesop_csv_anual_ABP_path))
print("bases anuais 2023 ate 01-10-2023 {}".format(aesop_csv_2023_path))
print("bases anuais de 02-10-2023 em diante {}".format(aesop_csv_2023_atual_path))
print("bases anuais de 02-10-2023 em diante {}".format(aesop_csv_2024_02dez_e_posterior))


#dado em parquet ate  
df_ate01122024 = spark.read.parquet(f"{escrita_aesop_to_parquet}/aesop_dados_2017_20241201.parquet/")

#novo schema a partir do arquivo semanal 02-12-2024 - add variável CO_CNES
schema_cnes = StructType(
   [StructField('ANO', IntegerType(), True),
    StructField('SEMANA', IntegerType(), True),
    StructField('SG_UF', StringType(), True),
    StructField('CO_MUNICIPIO_IBGE', IntegerType(), True),
    StructField('CO_CNES', IntegerType(), True),
    StructField('SEXO', StringType(), True),
    StructField('FX_ETARIA', StringType(), True),
    StructField('CIDCIAP', StringType(), True),
    StructField('QT', IntegerType(), True)
   ]
  )

df_2024_02_dez_atual = spark.read.options(header='True', delimiter=',')\
    .schema(schema_cnes)\
.csv(aesop_csv_2024_02dez_e_posterior)


df_2024_02_dez_atual = df_2024_02_dez_atual.withColumn("INPUT_FILE", F.input_file_name())\
.withColumn('Data_folder', F.regexp_extract('INPUT_FILE', '([0-9]{8})', 1))\
.withColumn("Data_folder",F.to_date(F.col("Data_folder"),"yyyyMMdd"))\
.drop('INPUT_FILE')

df_2024_02_dez_atual = df_2024_02_dez_atual.withColumn("ANO", F.col("ANO").cast(ShortType()))\
.withColumn("SEMANA", F.col("SEMANA").cast(ByteType()))

df_ate01122024 = df_ate01122024.withColumn("CO_CNES",F.lit(None))


df = df_ate01122024.unionByName(df_2024_02_dez_atual)
len(df.columns)

# %%
df.printSchema()
arquivo = pd.read_csv(nome_parquet, header=None)
content = arquivo.iloc[0, 0]

print(f'Local de escrita: {escrita_aesop_to_parquet}/aesop_dados_{content}')

df.write.parquet(f'{escrita_aesop_to_parquet}/aesop_dados_{content}.parquet', mode='overwrite')

# Finalize o trabalho Glue e pare a sessao Spark
job.commit()
spark.stop()
