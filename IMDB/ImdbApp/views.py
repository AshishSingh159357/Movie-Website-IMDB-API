from django.shortcuts import render
import requests
from multiprocessing import Pool,Process
import multiprocessing
import time
from django.http import HttpResponse
from django.shortcuts import redirect



taglines=[]
details=[]

headers = {
        'x-rapidapi-key': "0bf8ee38f6msh02e0adff8eb876ap18c767jsn520f8d6a1b74",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }



def overviewDetail(q):
    url3 = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    overview = requests.request("GET", url3, headers=headers, params=q)   
    return overview.json()
   


def detail(q):
    url2 = "https://imdb8.p.rapidapi.com/title/get-details"
    PopularMovieDetail = requests.request("GET", url2, headers=headers, params=q)
  
    return PopularMovieDetail.json()


def fullCredits(q):
    url = "https://imdb8.p.rapidapi.com/title/get-full-credits"
    response = requests.request("GET", url, headers=headers, params=q)
    return response.json()


def GetMoreLikeThis(q):
    url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"
    response = requests.request("GET", url, headers=headers, params=q)
    return response.json()


def News(q):
    url = "https://imdb8.p.rapidapi.com/title/get-news"
    response = requests.request("GET", url, headers=headers, params=q)
    return response.json()["items"]






# Create your views here.
def index(request):
    if request.method=="POST":
        KeyWord=request.POST.get("key-word")
        url = '{}{}'.format('movies/', KeyWord)
        return redirect(url)
 

    url = "https://imdb8.p.rapidapi.com/title/get-most-popular-movies"

    #this code is to get ID of popular movie

    querystring = {"homeCountry":"US","purchaseCountry":"US","currentCountry":"US"}

    popularMovieId = requests.request("GET", url, headers=headers, params=querystring)

    movies=popularMovieId.json()[:5]
    for i in range(len(movies)):
        movies[i]=movies[i][7:len(movies[i])-1]

    q=[]
    for j in movies:
        q.append({"tconst":j})

    #code for getting Id of popular web series
    urlPopularWeb="https://imdb8.p.rapidapi.com/title/get-most-popular-tv-shows"

    PopularWebId = requests.request("GET", urlPopularWeb, headers=headers, params=querystring)

    Web=PopularWebId.json()[:5]
    for i in range(len(Web)):
        Web[i]=Web[i][7:len(Web[i])-1]

    q2=[]
    for k in Web:
        q2.append({"tconst":k})

 
    # pool for getting detail of popular movie
    with Pool(3) as p:
        ii=p.map(overviewDetail, q)

    # pool for getting detail of popular web series
    
    with Pool(3) as p:
        WebSeries=p.map(overviewDetail, q2)

  

    # New
    with Pool(3) as p:
        news=p.map(News, q)

   
    for k in news[0]:
        #k['id']=k['id'][7:len(i['id'])-1]
        k['body']=k['body'][:40]
        k['head']=k['head'][:17]

    
   
    for i in ii:
        i['id']=i['id'][7:len(i['id'])-1]
    
   
    for j in WebSeries:
        j['id']=j['id'][7:len(j['id'])-1]
   
   
  

    return render(request,'index.html',{'detail':ii[:4],'WebSeries':WebSeries[:4],'news':news[0][:4]})
    #return render(request,'index.html')
   
    

    













def moviedetail(request,id):
    if request.method=="POST":
        KeyWord=request.POST.get("key-word")
        url = '{}{}'.format('movies/',KeyWord)
        return redirect(url)
   
    q={"tconst":id[:len(id)]}
    OverviewDetails=overviewDetail(q)

    cast=fullCredits(q)["cast"][:9]
    crew=fullCredits(q)["crew"]
    crew["producer"]=crew["producer"][:10]

    GMLT=GetMoreLikeThis(q)[:4]
    
   
    OverviewDetails["title"]["runningTimeInMinutes"]=str(OverviewDetails["title"]["runningTimeInMinutes"]/60)[:3]

    q=[]
    
    for i in range(len(GMLT)):
        GMLT[i]=GMLT[i][7:len(GMLT[i])-1]
    for j in GMLT:
        q.append({"tconst":j})

    with Pool(3) as p:
        ii=p.map(overviewDetail, q)

    for k in ii:
        k['id']=k['id'][7:len(k['id'])-1]
    

   
    #cast={'akas': ['Dave Batista', 'Deacon Batista', 'Batista', 'David Bautista'], 'id': '/name/nm1176985/', 'image': {'height': 562, 'id': '/name/nm1176985/images/rm1007918849', 'url': 'https://m.media-amazon.com/images/M/MV5BNTZkYzU0ZGUtZTk1MC00MzJjLWFmMzItY2M0ODY1ZmI2OGQ0XkEyXkFqcGdeQXVyMjI0MjgwNjc@._V1_.jpg', 'width': 1000}, 'legacyNameText': 'Bautista, Dave', 'name': 'Dave Bautista', 'billing': 1, 'category': 'actor', 'characters': ['Scott Ward'], 'roles': [{'character': 'Scott Ward'}]}
    
    return render(request,'MovieDetail.html',{'det':OverviewDetails,'cast':cast,'crew':crew,'detail':ii[:4]})
    #return render(request,'MovieDetail.html',{'det':OverviewDetails,'cast':cast})









def movies(request,KeyWord):
    if request.method=="POST":
        KeyWord=request.POST.get("key-word")
        url = '{}{}'.format('movies/',KeyWord)
        return redirect(url)

   
    url = "https://imdb8.p.rapidapi.com/title/find"
    querystring = {"q":KeyWord}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response=response.json()["results"]
    res=[]
    for i in response:
        i["id"]=i["id"][7:len(i["id"])-1]
        if "titleType" in i.keys():
            res.append(i)
    
    return render(request,'searchResult.html',{'response':res})
    #return render(request,'searchResult.html')