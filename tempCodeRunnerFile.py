from multiprocessing import Pool
import multiprocessing
import time


from django.shortcuts import render
import requests
import asyncio
import time

ii=[]
iii=[]

headers = {
        'x-rapidapi-key': "e12614f002mshaaa817c04f69c1dp178967jsnabda5708f551",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

def ss(q):
    url3 = "https://imdb8.p.rapidapi.com/title/get-taglines"
    taglineOfMovie = requests.request("GET", url3, headers=headers, params=q)
    #ii.append(taglineOfMovie.json())
    return taglineOfMovie.json()
    #return taglineOfMovie.json()


def ss2(q):
    url2 = "https://imdb8.p.rapidapi.com/title/get-details"
    PopularMovieDetail = requests.request("GET", url2, headers=headers, params=q)
    #iii.append(PopularMovieDetail.json())
    return PopularMovieDetail.json()



    
    
if __name__ == '__main__':
    start = time.time()
    detail=[]
    taglines=[]
    p=0
    
    url = "https://imdb8.p.rapidapi.com/title/get-most-popular-movies"

    #this code is to get ID of popular movie

    querystring = {"homeCountry":"US","purchaseCountry":"US","currentCountry":"US"}

    popularMovieId = requests.request("GET", url, headers=headers, params=querystring)


    #print(popularMovieId.json())
    movies=popularMovieId.json()[:5]
    for i in range(len(movies)):
        movies[i]=movies[i][7:len(movies[i])-1]


    q=[]
    for j in movies:
        q.append({"tconst":j})
    print(q)



    #print(ss(q[0]),ss2(q[0]))

    p=Pool()
    
    ii=p.map(ss, q)

    print()

    
    iii=p.map(ss2, q)

    end = time.time()

# total time taken
    print(f"Runtime of the program is {end - start}")
    




#sol1()




if ii!=[] and iii!=[]:    
    print("dsa",ii)
    print("sad",iii)



'''

def f(x):
    time.sleep(1)
    return x*x


if __name__ == '__main__':
    s=time.time()
    with Pool(3) as p:
        print(p.map(f, [1, 2, 3,4,5,6]))
    e=time.time()
    print(e-s)


if __name__ == '__main__':
    s=time.time()
    
   
    p1=multiprocessing.Process(target=f(3))
    p2=multiprocessing.Process(target=f(2))
    p3=multiprocessing.Process(target=f(4))

    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print([p1,p2,p3])

    e=time.time()
    print(e-s)

'''