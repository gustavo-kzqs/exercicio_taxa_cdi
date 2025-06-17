# utilizar o pandas e o seaborn para uma analise de dados de dois modos
# 1 - utilizar o terminal para processar os dados
# 2 - criar um script para automatizar os comandos

import os
import time
import json
import csv
from random import random
from datetime import datetime

import requests
import pandas as pd
import seaborn as sns
from sys import argv

import os
import time
import json
import csv
from random import random
from datetime import datetime

import requests
import pandas as pd
import seaborn as sns
from sys import argv

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados?formato=json'

def extrair_taxa():
    try:
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError:
        print("Dado não encontrado")
        return None
    except Exception as exc:
        print("Erro, parando a execução")
        raise exc
    else:
        return json.loads(response.text)[-1]['valor']

def gerar_csv():
    dado = extrair_taxa()

    if not os.path.exists('./taxa-cdi.csv'):
        with open('./taxa-cdi.csv', 'w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')

    for _ in range(0, 10):
        data_e_hora = datetime.now()
        data = data_e_hora.strftime('%Y/%m/%d')
        hora = data_e_hora.strftime('%H:%M:%S')
        cdi = float(dado) + (random() - 0.5)

        with open('./taxa-cdi.csv', 'a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi:.4f}\n')

        time.sleep(1)

    print("CSV gerado com sucesso")

def gerar_grafico(nome_grafico):
    df = pd.read_csv('./taxa-cdi.csv')
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    grafico.set_xticklabels(labels=df['hora'], rotation=90)
    grafico.figure.set_size_inches(12, 6)
    grafico.get_figure().savefig(f"{nome_grafico}.png")
    print(f"Grafico salvo como {nome_grafico}.png")

def main():
    if len(argv) < 2:
        print('Forneça o nome do grafico como parametro')
        return

    nome_grafico = argv[1]
    gerar_csv()
    gerar_grafico(nome_grafico)

if __name__ == "__main__":
    main()
              