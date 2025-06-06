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




#aesop_2017_2024 = spark.read.parquet(aesop_hpc_path+get_hpc_parquet_file_name())
#aesop_hpc_path+get_hpc_parquet_file_name()

aesop_2017_2024 = spark.read.parquet(f"{legada_path}/{content}_AESOP.parquet")
#aesop_2017_2024 = spark.read.parquet('/dados10t/datalake/standard/aesop/aesop_hpc/2017_20240114_AESOP.parquet/')

max_ano = aesop_2017_2024.agg(F.max("ano")).collect()[0][0]
semana_folder = aesop_2017_2024.filter(F.col("ano") == max_ano).agg(F.max("epiweek")).collect()[0][0]
(semana_folder, max_ano)

#semana_folder = 15 # remover isso, somente por conta do bug do dado que não teve semante corrente

aesop_report_folder  = "standard/reports/report_update/"

caminho_pasta = aesop_report_folder+"semana_"+str(semana_folder)+"_"+str(max_ano)
#caminho_pasta
create_folder_in_specific_location(bucket_name,caminho_pasta)

#df = spark.read.parquet(aesop_parquet_path+get_parquet_file_name())
#aesop_parquet_path+get_parquet_file_name()
#df = spark.read.parquet('/dados10t/datalake/raw/aesop/parquet_explorer/aesop_dados_2017_20240114.parquet/')
#df = spark.read.parquet("s3://fiocruz-datalake-bucket/raw/aesop/dados-ms-parquet/aesop_dados_2017_20240721.parquet/")

df = spark.read.parquet(f'{escrita_aesop_to_parquet}/aesop_dados_{content}.parquet/')
#df.count()

prefix = 'raw/aesop/dados_ms_originais/csv/semanal_02_dez_24_atual/'  # Caminho relativo dentro do bucket onde as pastas estão localizadas
try:
    dt_filtro_ultimo_dia = list_all_files_in_folders_s3(bucket_name, prefix)
    
except ValueError as e:
    print(e)


#dt_filtro_ultimo_dia = "20240324"
print("Data mais recente:", dt_filtro_ultimo_dia)
dt_filtro_ultimo_7dias = (datetime.strptime(dt_filtro_ultimo_dia, '%Y%m%d') - timedelta(days = 6)).strftime("%Y-%m-%d")
print(dt_filtro_ultimo_7dias)

df = df.filter((F.col("FX_ETARIA")).isNotNull())
df = df.filter(F.col("ANO") >= 2017)

# remove pontos da coluna de cidciap
df = df.withColumn("CIDCIAP", F.regexp_replace(F.col("CIDCIAP"), "\\.", ""))

# corta primeiros 4 digitos da colula CIDCIAP
df_CIDCIAP = df.withColumn('Codigo_CIDCIAP', F.substring('CIDCIAP', -5,5))
# remove parenteses da nova coluna
df_CIDCIAP = df_CIDCIAP.withColumn('Codigo_CIDCIAP_NEW', F.regexp_replace(F.col("Codigo_CIDCIAP"), "[\()]", ""))
# Use the split function to separate the string into two columns
df_CIDCIAP = df_CIDCIAP.withColumn("name_CIDCIAP", F.split(F.col("CIDCIAP"), "\\(").getItem(0))

# Define a condition to check the length of the text
condition = (F.length(F.col('Codigo_CIDCIAP_NEW')) == 4)
# cria codigo CIDCIAP de 3 letras
df_CIDCIAP = df_CIDCIAP.withColumn(
    'Codigo_CIDCIAP_NEW_FINAL',
    F.when(condition, F.expr("substring(Codigo_CIDCIAP_NEW, 1, length(Codigo_CIDCIAP_NEW)-1)"))
    .otherwise(F.col('Codigo_CIDCIAP_NEW'))
)

#concat acronimo with number
df_CIDCIAP = df_CIDCIAP.withColumn("Codigo_CIDCIAP_NEW_FINAL", F.concat_ws("", df_CIDCIAP["name_CIDCIAP"], df_CIDCIAP["Codigo_CIDCIAP_NEW_FINAL"]))
# dropa colunas temporarias
df_CIDCIAP = df_CIDCIAP.drop("Codigo_CIDCIAP","Codigo_CIDCIAP_NEW",'name_CIDCIAP')

codigos_ivas_numero = ['CIAPA03','CIAPR01','CIAPR02','CIAPR03','CIAPR04','CIAPR05','CIAPR07','CIAPR08','CIAPR21','CIAPR23','CIAPR25','CIAPR29','CIAPR71','CIAPR74','CIAPR75',
                       'CIAPR76','CIAPR77','CIAPR78','CIAPR80','CIAPR81','CIAPR83','CIAPR99','CIDJ00','CIDJ01','CIDJ02','CIDJ03','CIDJ04','CIDJ06','CIDJ09','CIDJ10',
                       'CIDJ11','CIDJ12','CIDJ13','CIDJ14','CIDJ15','CIDJ16','CIDJ17','CIDJ18','CIDJ20','CIDJ21','CIDJ22','CIDJ80','CIDR05','CIDR06','CIDR07','CIDR43',
                       'CIDR50','CIDU07','CIDB34','CIDB97']

df_IVAS = df_CIDCIAP.withColumn("atend_ivas", F.when( (F.col("Codigo_CIDCIAP_NEW_FINAL").isin(codigos_ivas_numero) ), F.col("QT")).otherwise(0))

codigos_ivas_exclusao = ['CID(R072)']
df_IVAS = df_IVAS.withColumn("atend_ivas", F.when( (F.col("CIDCIAP").isin(codigos_ivas_exclusao) ), 0).otherwise(F.col("atend_ivas")))

df_IVAS = df_IVAS\
.withColumn("Tipo_CIDCIAP", F.substring_index(df_IVAS.CIDCIAP, '(', 1))\
.withColumn("Codigo_CIDCIAP", F.substring_index(df_IVAS.CIDCIAP, '(', -1))

#remover paratese
df_IVAS = df_IVAS.withColumn("Codigo_CIDCIAP",F.regexp_replace("Codigo_CIDCIAP","\)",""))
#criar cid com 3 digitos
df_IVAS_v2 = df_IVAS.withColumn("Codigo_CIDCIAP_v2",F.when(F.col("Tipo_CIDCIAP") == "CID",F.substring("Codigo_CIDCIAP",1,3)  ).otherwise(F.col("Codigo_CIDCIAP")) )

#df_IVAS_v2.count()

#dt_filtro_ultimo_7dias

df_last_semana = df_IVAS_v2.filter(F.col("Data_folder") >= dt_filtro_ultimo_7dias)

#df_last_semana.count()

df_plot_last_semana = df_last_semana.groupBy("SEMANA", 'ANO').agg(F.sum("QT").alias("TOTAL"))

#df_IVAS_v2.orderBy(F.desc("Data_folder")).show(100)

#df_plot_last_semana.filter(F.col('ANO')==2024).show()

#caminho_pasta

#df_plot_last_semana.count()

#df_plot_last_semana.toPandas().to_parquet(aesop_report_folder +"semana_"+str(semana_folder)+ "/aesop_qt_ultima_semana.parquet") 
#aesop_report_folder +"semana_"+str(semana_folder)+ "/aesop_qt_ultima_semana.parquet"

#df_plot_last_semana.toPandas().to_parquet("s3://fiocruz-datalake-bucket/standard/reports/report_update/semana_12_2024/aesop_qt_ultima_semana.parquet")

path_salvar = "s3://fiocruz-datalake-bucket/"+caminho_pasta

df_plot_last_semana.toPandas().to_parquet(path_salvar+"/aesop_qt_ultima_semana.parquet")

reg_saude_br = spark.read.csv('s3://fiocruz-datalake-bucket/raw/aesop/dados_auxiliares/regiao_de_saude_brasil.csv',sep = ',', header='true')
reg_saude_br = reg_saude_br.withColumnRenamed("Cód IBGE","cod_IBGE")

df_mun_faltantes = df_last_semana

res = reg_saude_br.join(df_mun_faltantes, reg_saude_br.cod_IBGE == df_mun_faltantes.CO_MUNICIPIO_IBGE,'leftanti')

res_v2 = res.dropDuplicates(["cod_IBGE"])

#res_v2.select("UF","cod_IBGE","Município").toPandas().to_parquet(aesop_report_folder +"semana_"+str(semana_folder)+ "/mun_nao_enviaram_v2.parquet")
#aesop_report_folder +"semana_"+str(semana_folder)+ "/mun_nao_enviaram_v2.parquet"
res_v2.select("UF","cod_IBGE","Município").toPandas().to_parquet(path_salvar+"/mun_nao_enviaram_v2.parquet")

df_plot_tabela_cid_ciap = df_IVAS_v2.filter(F.col("ANO") == 2025).groupBy("SG_UF","Tipo_CIDCIAP","Codigo_CIDCIAP").agg(F.sum("atend_ivas").alias("atend_ivas")) #gerar plot por contribuição do cid

#df_plot_tabela_cid_ciap.toPandas().to_csv(aesop_report_folder +"semana_"+str(semana_folder)+"/aesop_tabela_codigos_uf_2024.csv",sep =";",index = False)
#aesop_report_folder +"semana_"+str(semana_folder)+"/aesop_tabela_codigos_uf_2024.csv"


df_plot_tabela_cid_ciap.toPandas().to_csv(path_salvar+"/aesop_tabela_codigos_uf.csv",sep =";",index = False)


df_plot_contrib = df_IVAS_v2\
.filter(F.col("ANO") >= max_ano-1)\
.filter((F.col("ANO") == max_ano) | (F.col("SEMANA") >= semana_folder))\
.groupBy("SEMANA", "ANO", "Codigo_CIDCIAP_v2", "Tipo_CIDCIAP")\
.agg(F.sum("atend_ivas").alias("atend_ivas")) #gerar plot por contribuição do cid

#df_plot_contrib.toPandas().to_csv(aesop_report_folder +"semana_"+str(semana_folder)+"/aesop_contribuicao_2024.csv",sep =";",index = False)
#aesop_report_folder +"semana_"+str(semana_folder)+"/aesop_contribuicao_2024.csv"

df_plot_contrib.toPandas().to_csv(path_salvar+"/aesop_contribuicao.csv",sep =";",index = False)


#%stop_session

# Finalize o trabalho Glue e pare a sessao Spark
job.commit()
spark.stop()

