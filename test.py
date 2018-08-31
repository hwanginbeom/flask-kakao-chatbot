import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/running/current.nhn"
req = requests.get(url).text
doc=BeautifulSoup(req , 'html.parser')#bs4 로 정제 파이썬이 해석을 할 수 있게끔 만든다.
title_tag=doc.select('dt.tit > a')
star_tag=doc.select('#content > div.article > div > div.lst_wrap > ul > li > dl > dd.star > dl.info_star > dd > div > a > span.num')
resever_tag=doc.select('#content > div.article > div > div.lst_wrap > ul > li > dl > dd.star > dl.info_exp > dd > div > span.num')
img_tag =doc.select('div.thumb > a > img')

#('div.star_t1>a>span.num')
#('div.star_t1.b_star>span.num') class 사이에 띄어쓰기가 있으면 . 으로 연결한다. 다른 클래스이다.

# star_list=[]
# resever_list=[]
# title_list=[]

movie_dict={}
# img_list=[]
# for i in img_tag:
#  img_list.append(i['src']) 

# print(img_list)

for i in range(0,10):
    movie_dict[i]={
        "title" : title_tag[i].text,
        "star" :star_tag[i].text,
        "resever":resever_tag[i].text,
        "image" : img_tag[i].get('src')
        # "image" : img_tag[i]['src']
    }
    # title_list.append(title_tag[i].text)
    # star_list.append(star_tag[i].text)
    # resever_list.append(resever_tag[i].text)

    
print(movie_dict)
# print(title_list)
# print(star_list)
# print(resever_list)