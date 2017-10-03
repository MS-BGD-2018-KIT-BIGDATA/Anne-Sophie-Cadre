import urllib
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import time

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

url='https://gist.github.com/paulmillr/2657075'
authperso=('user','password')

def get_top_contrib(url):
    soup = getSoupFromURL(url)
    l = []
    contribs = soup.find('tbody').find_all('tr')#.find(tbody).find_all(tr) puis foreach tr .find('a').text!!
    for c in contribs:
        name=c.find('a')
        if (name != None):
            l.append(name)
    return l

def MeanStars(own,authperso):
    repos = requests.get('https://api.github.com/users/'+own+'/repos', auth=authperso).json()
    
    nbRepo=0
    nbStar=0
    
    for repo in repos:
        stars=repo['stargazers_count']
        nbRepo+=1
        nbStar+=float(stars)
    if nbRepo==0:
        return 0
    else:
        return nbStar/nbRepo    

def getcontribwithstars(url,auth):
    contribsandstars=[]
    l=get_top_contrib(url)
    for contrib in l:
        contribsandstars.append((contrib,MeanStars(contrib,auth)))
    return sorted(contribsandstars, key=lambda tup: tup[1], reverse=True)

def getcontribsortedwithtime(url,auth):
    start_time = time.time()
    result=getcontribwithstars(url,auth)
    t=(time.time() - start_time)
    m=int(t//60)
    s=round(t-m*60)
    minutes=str(m)
    secondes=str(s)
    return (result, minutes + ' minutes et ' + secondes +' secondes')
