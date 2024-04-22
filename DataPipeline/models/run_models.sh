#!/bin/bash
#rodar modelos em R para o aesop , enviado caminhos para parametro , execução via terminal

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <caminho_para_input> <caminho_para_output>"
    exit 1
fi

# O primeiro argumento é o caminho do arquivo de input
INPUT_PATH="$1"

# O segundo argumento é o caminho do arquivo de output
OUTPUT_PATH="$2"


#ears


#Rscript 01_ears.R $INPUT_PATH $OUTPUT_PATH



#Rscript 02_glm.R $INPUT_PATH $OUTPUT_PATH

Rscript 03_bayes.R $INPUT_PATH $OUTPUT_PATH
