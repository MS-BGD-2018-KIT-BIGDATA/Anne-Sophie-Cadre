import urllib
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def med():
    iburesp = requests.get('https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprof%C3%A8ne').json()

    medicaments={}
    medicaments["Nom"]={}
    medicaments["Labo"]={}
    medicaments["Equivalent traitement"]={}
    medicaments["Année de commercialisation"]={}
    medicaments["Mois de commercialisation"]={}
    medicaments["Prix"]={}
    medicaments["Restriction age"]={}
    medicaments["Restriction poids"]={}
    
    for i,med in enumerate(iburesp):
        medre=requests.get('https://www.open-medicaments.fr/api/v1/medicaments/'+med['codeCIS'])
        medinfo=medre.json()
        medtext=medre.text

        #NOM
        medicaments["Nom"][i]=medinfo['denomination']

        #LABO
        lab=medinfo['titulaires']
        if len(lab)>0:
            medicaments["Labo"][i]=lab[0]
        else:
            medicaments["Labo"][i]=None
            
        #EQUIVALENT TRAITEMENT
        desi=medinfo['compositions'][0]['designationElementPharmaceutique']
        reference=medinfo['compositions'][0]['referenceDosage']
        dosage=medinfo['compositions'][0]['substancesActives'][0]['dosageSubstance']
        nbr=medinfo['presentations'][0]['libelle']

        eq_traitement=None

        def doze(dos,unit):
            dose=int(re.findall('[0-9]+',dos)[0])
            if len(re.findall('m'+unit,dos))>0:
                dose=dose*0.001
            return dose

            #SI C'EST UN COMPRIME

        if desi=='comprimé':

            nbr_comprime=int(re.findall('[0-9]+',nbr)[0])
            eq_traitement=doze(dosage,'g')*nbr_comprime

            #SI C'EST UN GEL

        elif desi =='gel':
            ref=doze(reference,'g')

            nbr_tube,g_tube=int(re.findall('[0-9]+',nbr)[0]),int(re.findall('[0-9]+',nbr)[1])

            if len(re.findall('mg',nbr))>0:
                g_tube=g_tube*0.001

            dose=doze(dosage,'g')

            eq_traitement=nbr_tube*g_tube*dose/ref

            #SI C'EST UNE SOLUTION

        elif desi=='solution':
            ref=doze(reference,'l')

            nbr_flacon,ml_flacon=int(re.findall('[0-9]+',nbr)[0]),int(re.findall('[0-9]+',nbr)[1])

            if len(re.findall('ml',nbr))>0:
                ml_flacon=ml_flacon*0.001

            dose=doze(dosage,'g')

            eq_traitement=nbr_flacon*ml_flacon*dose/ref

        else: 
            print("Ni une solution, ni un gel, ni un comprimé... quoi donc ?")
            print(desi)

        medicaments["Equivalent traitement"][i]=eq_traitement

        #ANNEE DE COMMERCIALISATION
        date=medinfo['presentations'][0]['dateDeclarationCommercialisation']
        medicaments["Année de commercialisation"][i]=re.findall('([0-9]{4})-',date)[0]

        #MOIS DE COMMERCIALISATION
        medicaments["Mois de commercialisation"][i]=re.findall('-([0-9]{2})-',date)[0]
        
        #PRIX
        medicaments["Prix"][i]=medinfo['presentations'][0]['prix']

        #RESTRICTION AGE
        age=re.findall("plus de ([0-9]+) ans",medtext)
        agerestr=None
        if len(age)>0:
            agerestr=age[0]
        
        medicaments["Restriction age"][i]=agerestr

        #RESTRICTION POIDS
        medicaments["Restriction poids"][i]=None
        
    return pd.DataFrame(medicaments)[["Nom","Labo","Equivalent traitement","Année de commercialisation","Mois de commercialisation","Prix","Restriction age","Restriction poids"]]    

med()
