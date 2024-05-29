#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#
# Script    : BKP_Anuncios.py
# Author    : Fernando Altava de Lima 
# e-mail    : fadelima@avaya.com
# Author    : Icaro Silva Nunes
# e-mail    : inunesdasilv@avaya.com
# Version   : 1.0 - MAY/27/2024
# Method    : This program was created to find and backup AMS announcements.
# Method    : os arquivos serão salvos na pasta /tmp/anuncios_c-
#
#################################################################################
import os
import sys
import csv
######################################################################
#procura a pasta com o maior numero de arquivos dentro da pasta e copiados
#todos os arquivos que começam com c- e os copia em /tmp/anuncios_c-
def copy_files():
    # Define os diretórios de origem e destino
    source_dir = '/opt/avaya/mediaserver/ma/MAS/platdata/CStore/StorageRoot'
    target_dir = '/tmp/anuncios_c-'

    # Verifica se o diretório de destino existe, senão cria
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Obtém a pasta com o maior número de arquivos
    max_folder = ''
    max_count = 0
    for root, dirs, files in os.walk(source_dir):
        file_count = len([f for f in files if f.startswith('c-')])
        if file_count > max_count:
            max_count = file_count
            max_folder = root

    if max_folder:
        # Copia os arquivos para o diretório de destino
        for file_name in os.listdir(max_folder):
            if file_name.startswith('c-'):
                source_file = os.path.join(max_folder, file_name)
                target_file = os.path.join(target_dir, file_name)
                with open(source_file, 'rb') as src, open(target_file, 'wb') as dest:
                    dest.write(src.read())
        print("Arquivos copiados com sucesso.")
    else:
        print("Nenhuma pasta encontrada com arquivos que começam com 'c-'.")

if __name__ == "__main__":
    copy_files()
########################################################
#roda a query e salva o resultado no .txt
def run_mysql_command():
    command = "mysql -u platdbuser -pplatdbpass -D emcstore -e \"select filename, contentid from cs_content_meta where filename like 'c%';\""
#    os.system(command)

    try:
        result = os.popen(command).read()
        
        # Exibir resultado no terminal
#        print(result)

        # Salvar resultado em /tmp/anuncios.txt
        with open('/tmp/.anuncios.txt', 'w') as file:
            file.write(result)

#        print("Resultado salvo em /tmp/.anuncios.txt.")

    except Exception as e:
        print("Ocorreu um erro: {e}")

if __name__ == "__main__":
    run_mysql_command()
########################################################
#cria arquivo .csv correto a partir do um .txt 
def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as f_input:
        with open(output_file, 'w') as f_output:
            # Ler linhas do arquivo de texto
            for line in f_input:
                # Remover espaços em branco extras e dividir os valores
                values = line.strip().split()
                # Escrever os valores no arquivo CSV separados por vírgula
                f_output.write(','.join(values) + ".wav"+ '\n')

# Chamada da função para converter o arquivo txt em csv
txt_to_csv('.anuncios.txt', '.anuncios.csv')
##########################################################################
#renomeia os anuncios
def rename_files_based_on_csv(csv_file, folder_path):
    # Abrir o arquivo CSV
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pular o cabeçalho, se houver

        # Iterar sobre as linhas do CSV
        for row in reader:
            old_name = os.path.join(folder_path, row[0])
            new_name = os.path.join(folder_path, row[1])

            # Verificar se o arquivo antigo existe e renomeá-lo
            if os.path.exists(old_name):
                os.rename(old_name, new_name)

# Caminho para o arquivo CSV e pasta contendo os arquivos
csv_file = '/tmp/.anuncios.csv'
#o arquivo deve conter arquivo_antigo.wav,arquivo_novo.wav
folder_path = '/tmp/anuncios_c-'

# Chamar a função para renomear os arquivos
rename_files_based_on_csv(csv_file, folder_path)
################################################################################
