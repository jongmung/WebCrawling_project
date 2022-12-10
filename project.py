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

df = pd.DataFrame(columns=['글자수','이미지수','제목','발행일'])

for cnt, i in enumerate(lis):
    print(f"블로그{cnt+1} / 전체블로그 {len(lis)}")
    link = i.select_one("a.api_txt_lines.total_tit").get("href")
    thumb = i.select_one("a.sub_thumb").get("href")
    
    uid = thumb.split("/")[-1]
    logNo = link.split("/")[-1]
    
    if ((not uid.strip())or (not logNo.strip())):
        continue
    
    post_url = f"https://blog.naver.com/PostView.naver?blogId={uid}&logNo={logNo}"
    print (post_url)
    r = requests.get(post_url, headers=header)
    bs = BeautifulSoup(r.txt, "lxml")