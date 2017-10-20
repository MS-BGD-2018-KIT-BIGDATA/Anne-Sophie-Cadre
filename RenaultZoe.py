import urllib
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

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
    
url="https://www.leboncoin.fr"

typeannonce="voitures"
région="ile_de_france"

def getLinks(website,type_annonce,région,recherche):
    l=[]
    
    #Create url-link
    page=0
    rech=recherche.replace(" ","%20").replace("é","%E9").replace("è","%E8").replace("à","%E0")
    url = website +"/"+type_annonce+"/offres/"+région+"/"+"?o="
    suite = "&q="+rech
    links=["yo"]
    
    while links != None: 
        soup = getSoupFromURL(url+str(page)+suite)
        lin = soup.find('section',class_='tabsContent')
        if lin == None:
            break
        else:
            links = lin.find_all('a')
            for link in links:
                if link.has_attr('href'):
                    a = link.attrs['href']
                    if a not in l:
                        l.append(a)
        page+=1    
    return l

import re

def getResults(liste):
    
    #Initialisation du tableau des données
    cars={}
    cars["Version"]={}
    cars["Kilomètrage"]={}
    cars["Année"]={}
    cars["Prix"]={}
    cars["Téléphone"]={}
    cars["Pro"]={}
    cars["Cote"]={}
    cars["Différence"]={}
    
    for i,car in enumerate(liste):
        s=getSoupFromURL("https:"+car)
        soup=s.text.lower()
        
        
        #VERSION
        version=re.findall("(life|intens|zen)",soup)
        if len(version)!=0:
            cars["Version"][i]=version[0]
        else:
            cars["Version"][i]=None
        
        #KM
        km=re.findall("km : \"([0-9]+)\",", soup)
        if len(km)!=0:
            cars["Kilomètrage"][i]=int(km[0])
        else:
            cars["Kilomètrage"][i]=None
        
        #ANNEE
        annee=re.findall("annee : \"([0-9]+)\",", soup)
        if len(annee)!=0:
            cars["Année"][i]=int(float(annee[0]))
        else:
            cars["Année"][i]= None
        
        #PRIX
        prix=re.findall("prix : \"([0-9]+)\",",soup)
        if len(prix)!=0:
            cars["Prix"][i]=int(float(prix[0]))
        else:
            cars["Prix"][i]= None
         
        
        #TEL
        tel=re.findall("((\+\d+(\s|-))?0\d(\s|-)?(\d{2}(\s|-)?){4})",soup)
        if len(tel)!=0:
            cars["Téléphone"][i]=tel[0][0].replace('\n','')
        else:
            cars["Téléphone"][i]=None
        
        #PRO
        pro=re.findall("(pro véhicules)",soup)
        if len(pro)!=0:
            cars["Pro"][i]="Oui"
        else:
            cars["Pro"][i]="Non"
        
        #COTE 
        if len(annee)!=0 and len(version)!=0:
            urlcote="https://www.lacentrale.fr/cote-auto-renault-zoe-"+version[0]+"-" + str(annee[0]) + ".html"
            soupcote=getSoupFromURL(urlcote).find('span',class_='jsRefinedQuot')
            if soupcote!=None:
                cars["Cote"][i]=int(float(soupcote.text.replace(" ","")))
            else:
                cars["Cote"][i]=None
        else:
            cars["Cote"][i]=None
        
        #DIFFERENCE
        if cars["Cote"][i]==None or cars["Prix"][i]==None:
            cars["Différence"][i]="No Data"
        else:
            if cars["Cote"][i]>cars["Prix"][i]:
                cars["Différence"][i]="Prix supérieur à la cote"
            else:
                cars["Différence"][i]="Prix inférieur à la cote"
            
    return pd.DataFrame(cars)

test=getLinks(url,"voitures",région,"Renault Zoe")+getLinks(url,"voitures","provence_alpes_cote_d_azur","Renault Zoe")+getLinks(url,"voitures","aquitaine","Renault Zoe")
len(test)

df=getResults(test)

df
