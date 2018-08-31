import os
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request


app= Flask(__name__)

@app.route('/')
def hello():
    return '여기는 챗봇 페이지 입니다.'

@app.route('/keyboard')
def keyboard():
    keyboard ={
    "type" : "buttons",
    "buttons" : ["메뉴", "로또", "고양이","영화"]}
    return jsonify(keyboard)
    
@app.route('/message', methods=['POST']) # post 방식으로 들어온다. message 를타고 
def message():
    user_msg=request.json['content']     # content를 넣고 
    img_bool=False
    if user_msg =="메뉴":
        menu = ["시골길","20층","김가네","소풍김밥"]
        return_msg = random.choice(menu)
    elif user_msg =="로또":
        lotto=list(range(1,46))
        pick=random.sample(lotto,6)
        return_msg= str(sorted(pick))
        
    elif user_msg =="고양이":
        img_bool=True
        url ="https://api.thecatapi.com/v1/images/search?mime_types=jpg"
        req=requests.get(url).json()
        return_img=req[0]['url']
        return_msg="예비 집사님"
        
    elif user_msg == "영화":
        img_bool=True
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
        pick_movie = movie_dict[random.randrange(0,10)]
        return_msg="제목 :{}, 별점 {}, 예매율"
        return_msg="%s/평점:%s/예매율:%s" % (pick_movie['title'],pick_movie['star'],pick_movie['resever'])
        return_img=pick_movie['image']
        
        
    else :
        return_msg = "메뉴만 사용가능!"

    if img_bool==False:
        return_json={
            "message" : {
                "text": return_msg
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이","영화"]
            }
        }
    else:
        return_json={
            "message" : {
                "text": return_msg,
                "photo" : {
                    "url":return_img ,
                    "height": 630,
                    "width": 720
                }
                
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : ["메뉴", "로또", "고양이","영화"]
            }
        }
    
    return jsonify(return_json)
    
app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',8080)))