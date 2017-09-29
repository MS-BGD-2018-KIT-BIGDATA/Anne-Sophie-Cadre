import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from numpy import mean

url='https://www.cdiscount.com/search/10/ordinateur+portable.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=0&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets%5B3%5D=f%2F6%2Facer&FacetForm.SelectedFacets%5B3%5D=f%2F6%2Fdell&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&FacetForm.SelectedFacets.Index=14&FacetForm.SelectedFacets.Index=15&FacetForm.SelectedFacets.Index=16&FacetForm.SelectedFacets.Index=17&FacetForm.SelectedFacets.Index=18&FacetForm.SelectedFacets.Index=19&SortForm.SelectedNavigationPath=&ProductListTechnicalForm.Keyword=ordinateur%2Bportable&&_his_'

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

def createfloat(a):
    if "€" in a:
        b=float(a.replace("€","."))
    if "," in a:
        b=float(a.replace(",","."))
    return b

def findbest(brande1,brande2,url):
    soup = getSoupFromURL(url)
    
    brand1=brande1.lower()
    brand2=brande2.lower()
    
    #Find the "blocs" of each products
    blocs = soup.find_all('div', class_='prdtBloc')
    
    #Find the interesting elements in these blocs
    br1 = []
    br2 = []
    for b in blocs:
        pp = b.find('div',class_='prdtPrSt')
        p = b.find('span',class_='price')
        t = b.find('div',class_='prdtBTit')
        if t != None:
            title = t.text.strip()
        if p != None:
            price = createfloat(p.text.strip())
        if pp != None:
            previousprice = createfloat(pp.text.strip())
        else:
            previousprice = price
            
        if brand1 in title.lower():
            br1.append(((previousprice-price)/previousprice)*100)
        if brand2 in title.lower():
            br2.append(((previousprice-price)/previousprice)*100)

    if mean(br1)>mean(br2):
        result= "Les réductions de "+brande1+ " sont meilleures"
    else:
        result= "Les réductions de " +brande2+ " sont meilleures"
        
    return result
    
findbest('acer','dell',url)
