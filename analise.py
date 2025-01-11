# bibliotecas de extracao
import os, json, requests
from random import random
from datetime import datetime
from time import sleep

# bibliotecas de visualizacao
import csv, pandas as pd, seaborn as sns
from sys import argv

#lib externa
from lib.exceptionhandler import exceptionhandler as exch

def extrair_cdi():
    print("Obtendo taxa CDI...")
    URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

    # Capturando a taxa CDI (fonte: api do banco central)

    try:
        response = requests.get(url = URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        exch(status = "alert", message = "Dado não encontrado, continuando.", prefix = "Alerta: ")
        cdi = None
    except Exception as exc:
        exch(status = "error", message = "Parando a execução.", prefix = "ERRO: ")
        raise exc
    else:
        dado = json.loads(response.text)[-1]['valor']

    # Armazenando data e hora atual

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        # Verificando se "taxa-cdi.csv" existe

        if os.path.exists('./taxa-cdi.csv') == False:
            print("Arquivo taxa_cdi.csv não existe. Criando um novo arquivo...")

            with open(file='./taxa-cdi.csv', mode = 'w', encoding='utf8') as fp:
                fp.write('data,hora,taxa\n') # escrevendo cabecalho

            # Salvando dados no arquivo "taxa-cdi-csv"

        with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
            fp.write(f"{data}, {hora}, {cdi}")
        
        sleep(1)

    exch(message = "Taxa CDI capturada com sucesso.", status = "ok" )

    sleep(1)


def exportar_dados(dados: str, nome_saida: str):
    # carregando dataframe
    df = pd.read_csv(dados)

    # Salvando no grafico

    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    _ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.get_figure().savefig(f"{nome_saida}.png")



extrair_cdi()

try:
    exportar_dados(dados = "./taxa-cdi.csv", nome_saida = argv[1])
except IndexError:
    exch(message = "Falha ao exportar o gráfico. Argumentos Inválidos", status = "error", prefix = "ERRO: ")
else:
    exch(message = "Gráfico exportado com sucesso.", status = "OK")
