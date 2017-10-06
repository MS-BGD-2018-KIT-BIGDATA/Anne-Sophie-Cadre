import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from numpy import mean

url= 'https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peuplées'

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

def get_cities(n):
    soup = getSoupFromURL(url)
    lines=soup.find('table', class_='wikitable sortable').find_all('tr')
    liste=[]

    for cit in lines:
        city=cit.find('a')
        if city != None:
            liste.append(city.text)
            
    return "|".join([i.replace(' ','+') for i in liste[1:n+1]])

def getdist(villes):
    API_KEY='&key=AIzaSyDpie9dBUJ_YGVio7CSYuzq4HGkIt6Ie-Q'
    API_Adrr='https://maps.googleapis.com/maps/api/distancematrix/json?mode=driving'
    API_origin = '&origins='
    API_dest='&destinations='    

    dists = requests.get(API_Adrr+API_origin+origidest+API_dest+origidest)
    
    return dists

def get_distance_matrix(distance):
    distances=distance.json()
    distance_matrix={}
    origidest=[i.split(',')[0] for i in distances['destination_addresses']]
    rows=distances['rows']
    for i, origin in enumerate(origidest):
        distance_matrix[origin]={}
        for j, destination in enumerate(origidest):
            if j<=i:
                value=rows[i]['elements'][j]['distance']['value']
                distance_matrix[origin][destination]=value
                distance_matrix[destination][origin]=value
            else:
                break
    return distance_matrix

def create_df(distance_matrix):
    return pd.DataFrame(distance_matrix)

table=create_df(get_distance_matrix(getdist(get_cities(10))))
table.to_csv('distances.csv',sep=';')

table
