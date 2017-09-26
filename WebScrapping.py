import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

url2013='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013'
url2012='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2012'
url2011='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2011'
url2010='http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2010'

def getSoupFromURL(url, method='get', data={}):
    if method == 'get':
        res = requests.get(url)
    elif method == 'post':
        res = requests.post(url, data=data)
    else:
        return None
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None

el=["TOTAL DES PRODUITS DE FONCTIONNEMENT = A","TOTAL DES CHARGES DE FONCTIONNEMENT = B","TOTAL DES RESSOURCES D'INVESTISSEMENT = C"]

def extract(url,liste):
    soup=getSoupFromURL(url)
    year=soup.find('tr', class_='bleu G').find_all('td')[2].text.strip()
    data=soup.find_all('tr', class_='bleu')
    l=[]
    for i in range(0,len(data)-1):
        d=data[i].find(class_="libellepetit")
        if d != None: 
            if d.text.strip() in el:
                l.append(i)
    EPH=[]
    MDS=[]
    OP=[]
    for i in l:
        OP.append(data[i].find(class_="libellepetit").text.strip())
        MDS.append(data[i].find_all(class_="montantpetit G")[1].text.strip())
        EPH.append(data[i].find_all(class_="montantpetit G")[2].text.strip())
    df=pd.DataFrame(index=OP)
    df['Euros par habitant']=EPH
    df['Moyenne de la strate']=MDS
    print(year)
    return df

extract(url2010,el)
extract(url2011,el)
extract(url2012,el)
extract(url2013,el)
