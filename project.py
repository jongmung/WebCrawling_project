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

df = pd.DataFrame(columns=['식당이름','제목','위치','발행일','공감'])

for cnt, i in enumerate(lis):
    print(f"블로그{cnt+1} / 전체블로그 {len(lis)}")
    if cnt > 2:
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
        eatery = bs.select_one("div.se-module-map-text > a > strong.se-map-title").text
        title = bs.select_one("div.pcol1 > div > p > span").text
        pub_date = bs.select_one("div.blog2_container > span.se_publishDate").text
        #contents = bs.select_one("div.se-main-container").text.replace("\n", "")
        #images = bs.select_one("div.se-main-container").select("img")
        locate = bs.select_one("div.se-module-map-text > a > p.se-map-address").text
        heart = bs.select_one("div.u_likeit_list_module > span.u_likeit_list_btn > em.u_txt").text
        #heart_len = len(heart)
        #total_len = len(contents)
        #img_len = len(images)
        print(f"식당이름: {eatery} 제목: {title} 위치 : {locate} 발행일 : {pub_date} 공감 : {heart}")
        #print(f"데이터: {container}")
        df = df.append(pd.DataFrame([[eatery, title, locate, pub_date, heart]], columns=['식당이름','제목', '위치', '발행일', '공감']), ignore_index=True)
        
print(df)
df.to_csv('./Food_blog.csv', encoding='utf-8')