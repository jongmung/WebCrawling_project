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

df = pd.DataFrame(columns=['글자수','이미지수','제목','발행일','위치'])

for cnt, i in enumerate(lis):
    print(f"블로그{cnt+1} / 전체블로그 {len(lis)}")
    if cnt > 10:
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
        title = bs.select_one("div.pcol1 > div > p > span").text
        pub_date = bs.select_one("div.blog2_container > span.se_publishDate").text
        contents = bs.select_one("div.se-main-container").text.replace("\n", "")
        images = bs.select_one("div.se-main-container").select("img")
        locate = bs.select_one("div.se-module-map-text").text
        total_len = len(contents)
        img_len = len(images)
        print(f"전체 글자수: {total_len} 이미지갯수: {img_len} 제목: {title} 발행일 : {pub_date} 위치 : {locate}")
        #print(f"데이터: {container}")
        df = df.append(pd.DataFrame([[total_len, img_len, title, pub_date, locate]], columns=['글자수', '이미지수', '제목', '발행일', '위치']), ignore_index=True)
        
print(df)
df.to_csv('./Food_blog.csv', encoding='utf-8')