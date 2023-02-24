import requests
import json
import pandas as pd

with open('paises_siglas.json', encoding="utf8") as fp:
    paises_siglas = json.load(fp)
with open('atb_codes.json', encoding="utf8") as fp:
    atributos_cods = json.load(fp)
with open('commmodities_codes.json',encoding="utf8") as fp:
    comms = json.load(fp)

headers = {'API_KEY' :'5CC2E390-B4D1-46A6-9E6F-C7F6132E61C7'}

def get_data_countrie(com: str, pais: str, ano: str):
    #Utilizando um hashmap com os dicionarios de códigos de commodities, siglas de países e códigos de atributos, a função gera um dataframe.
    com_code, cod_pais  =  comms[com]['cod'], paises_siglas[pais]
    jsonData = requests.get(url = str(f'https://apps.fas.usda.gov/OpenData/api/psd/commodity/{com_code}/country/{cod_pais}/year/{ano}'), headers=headers).json()
    df = pd.read_json(json.dumps(jsonData))
    df['Nome_pais'] = pais 
    df['atributos'] = df['attributeId'].apply(lambda x: atributos_cods[str(x)]['nm_pt'])
    return df

def get_data_world(com, ano):
    #O caminho para fazer requisiçoes com dados agregados para o mundo como um todo é um pouco diferente da url para dados por países, mas a logica é a mesma.
    com_code =  comms[com]['cod']
    jsonData = requests.get(url = str(f'https://apps.fas.usda.gov/OpenData/api/psd/commodity/{com_code}/world/year/{ano}'), headers= headers).json()
    df = pd.read_json(json.dumps(jsonData))
    df['Nome_pais'] = 'Mundo'
    df['atributos'] = df['attributeId'].apply(lambda x: atributos_cods[str(x)]['nm_pt'])
    return df