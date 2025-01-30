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
    #metodo que monta e exporta o arquivo taxa-cdi.csv
    def montar_csv(dados, linhas: int):
        try:
            with open(file = './taxa-cdi.csv', mode = 'w', encoding='utf8') as fp:
                print("Salvando em taxa-cdi.csv")
                #escrevendo cabeçalho
                fp.write('Data,Valor\n')
                
                #preenchendo arquivo com os dados
                # mes e ano atual, importante para reorganizar os dados a serem exportados
                data_atual = datetime.strftime(datetime.now(), '%Y/%m/%d').split(sep = "/")
                ano = int(data_atual[0])
                mes = int(data_atual[1])
                for i in range(linhas, 0, -1): # laço for funciona em ordem descrescente
                    data_requisicao = f"01/{mes:02}/{ano}"

                    linha_encontrada = None
                    for item in dados:
                        if item['data'] == data_requisicao:
                            linha_encontrada = item
                            fp.write(f"{item['data']},{float(item['valor'])}\n") # escrevendo linha
                    
                    mes -=1
                    
                    if mes == 0:
                        mes = 12
                        ano -= 1
        except Exception as exc:
            #caso aconteça um erro, ele vai passar pelo exch
            exch(status = "error", message = f"{exc}", prefix = "ERRO") 
            raise exc
        else:
            #tudo deu certo.
            exch(message = "'taxa-cdi.csv' salvo com sucesso.", status = "ok" )


    print("Obtendo taxa CDI...")
    URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

    # Capturando a taxa CDI (fonte: api do banco central)

    try:
        response = requests.get(url = URL)
        response.raise_for_status()
    except requests.HTTPError as exc:
        #retorna um aleta em caso de HTTPError
        exch(status = "alert", message = "Dado não encontrado, continuando.", prefix = "Aviso")
        cdi = None
    except Exception as exc:
        #houve um erro, o codigo para imediatamente
        exch(status = "error", message = "Parando a execução.", prefix = "ERRO")
        raise exc
    else:
        # prosseguindo com o processamento...
        qtd_registros = 0
        
        dados = json.loads(response.text)
        exch(status = "ok", message = "Dados da api carregados com sucesso!")
        for linha in dados:
            qtd_registros += 1

        print(f"""
Foram encontradas {qtd_registros} registros no banco de dados, selecione uma opção:.

1. Exportar todos os registros
2. Exportar os ultimos 12 registros (recomendado)
3. Exportar uma quantidade especifica de registros              
            """)
        while True:
            escolha = int(input("Opção: "))

            if escolha == 1:
                montar_csv(dados = dados, linhas = qtd_registros)
                break
            elif escolha == 2:
                montar_csv(dados = dados, linhas = 12)
                break
            elif escolha == 3:
                qtd_escolhida = int(input("Digite a quantidade de registros: "))
                montar_csv(dados = dados, linhas = qtd_escolhida)
                break
            else:
                exch(status = "error", message = "Opção inválida, tente novamente", prefix = "ERRO")
                continue
            
        sleep(1)


def exportar_dados(dados: str, nome_saida: str):
    # carregando dataframe
    df = pd.read_csv(dados)

    # Salvando no grafico

    grafico = sns.lineplot(x=df['Data'], y=df['Valor'])
    _ = grafico.set_xticklabels(labels=df['Data'], rotation=30)
    grafico.get_figure().savefig(f"{nome_saida}.png")


extrair_cdi() #método extrair_cdi não precisa de parâmetros

# retorna ao usuário caso o argumento pro nome do gráfico for inválido
try:
    exportar_dados(dados = "./taxa-cdi.csv", nome_saida = argv[1])
except IndexError:
    exch(message = "Falha ao exportar o gráfico. Argumentos Inválidos", status = "error", prefix = "ERRO")
else:
    #deu tudo certo
    exch(message = "Gráfico exportado com sucesso.", status = "OK")
