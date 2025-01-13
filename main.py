# bibliotecas de extracao
import os, json, requests
from random import random
from datetime import datetime
from time import sleep

# bibliotecas de visualizacao
import csv, pandas as pd, seaborn as sns
from sys import argv

#lib interna
from lib.exceptionhandler import exceptionhandler as exch

def extrair_cdi():
    """
    def montar_csv(dados):

        # verifica se o arquivo taxa-cdi ja existe
        if os.path.exists("./taxa-cdi.csv"):
            with open
            
            for i in range(1, 11):
                print(dados[-i])
    """


    print("Obtendo taxa CDI...")
    URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

    # Capturando a taxa CDI (fonte: api do banco central)

    try:
        response = requests.get(url = URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        exch(status = "alert", message = "Dado não encontrado, continuando.", prefix = "Aviso")
        cdi = None
    except Exception as exc:
        exch(status = "error", message = "Parando a execução.", prefix = "ERRO")
        raise exc
    else:
        escolha = None
        qtd_datas = 0
        
        dados = json.loads(response.text)
        
        for linha in dados:
            qtd_datas += 1

        print(f"""{qtd_datas} datas encontradas""")
    #exch(message = "Taxa CDI capturada com sucesso.", status = "ok" )

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
    exch(message = "Falha ao exportar o gráfico. Argumentos Inválidos", status = "error", prefix = "ERRO")
else:
    exch(message = "Gráfico exportado com sucesso.", status = "OK")
