from contextlib import nullcontext
import requests
from bs4 import BeautifulSoup
import pandas as pd

header = {"user-agent": "Mozilla/5.0"}
keyword = input("검색할 내용을 입력해주세요 >> ")
url = f"https://search.naver.com/search.naver?query={keyword+' 맛집'}&nso=&where=blog&sm=tab_opt"
print(url)

r = requests.get(url, headers=header)
bs = BeautifulSoup(r.text, "lxml")
#print(bs)
lis = bs.select("ul.lst_total > li.bx")

df = pd.DataFrame(columns=['식당이름','제목','위치','발행일','댓글수'])

for cnt, i in enumerate(lis):
    print(f"블로그{cnt+1} / 전체블로그 {len(lis)}")
    if cnt > 5:
        break
    link = i.select_one("a.api_txt_lines.total_tit").get("href")
    thumb = i.select_one("a.sub_thumb").get("href")
    
    uid = thumb.split("/")[-1]
    logNo = link.split("/")[-1]
    
    if ((not uid.strip())or (not logNo.strip())):
        continue
    
    post_url = f"https://blog.naver.com/PostView.naver?blogId={uid}&logNo={logNo}"
    print (post_url)
    r = requests.get(post_url, headers=header)
    bs = BeautifulSoup(r.text, "lxml")
    #print(bs)
    
    if (bs.select_one("div.pcol1 > div > p > span") is None):
        continue
    else:
        eatery = bs.select_one("div.se-module-map-text > a > strong.se-map-title").text #식당이름
        title = bs.select_one("div.pcol1 > div > p > span").text                        #블로그제목
        pub_date = bs.select_one("div.blog2_container > span.se_publishDate").text      #발행일
        locate = bs.select_one("div.se-module-map-text > a > p.se-map-address").text    #위치
        if (bs.select_one("a.btn_comment > em._commentCount") is None):                 #댓글
            post = "x"
        else:
            post = bs.select_one("a.btn_comment > em._commentCount").text
        #만약 블로그 댓글기능이 제한이라면 x
        #달려있는 댓글이 없는 상태라면 빈칸

        print(f"식당이름: {eatery} 제목: {title} 위치 : {locate} 발행일 : {pub_date}  댓글수 : {post}")
        df = df.append(pd.DataFrame([[eatery, title, locate, pub_date,  post]], columns=['식당이름','제목', '위치', '발행일','댓글수']), ignore_index=True)
        
print(df)
df.to_csv('./맛집리스트.csv', encoding='utf-8')