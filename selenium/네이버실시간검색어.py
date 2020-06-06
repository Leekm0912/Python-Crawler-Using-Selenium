from bs4 import BeautifulSoup
from selenium import webdriver
import time

chrome_version = "80"
path = "D:\FTP\Personal_study\Python\웹크롤링\셀레니움\chromedriver_win32_v"+chrome_version+"\chromedriver.exe"

driver = webdriver.Chrome(path)
# 웹페이지 로딩까지 기다릴 시간(초). 너무 빠르면 못찾을때도 있음.
driver.implicitly_wait(10)
driver.get('https://datalab.naver.com/keyword/realtimeList.naver')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#ul중 class가 ranking_list태그의 자손중 span태그이고 class가 item_title인것.
title = soup.select('ul.ranking_list span.item_title')

now_time = time.strftime('%y%m%d-%H%M%S', time.localtime(time.time()))
#title에서 text 부분만 뽑아서 print
with open(now_time+".txt","w",encoding="utf-8") as w:
    num = 1
    for i in title:
        print(str(num)+"위 : " + i.text)
        w.write(str(num)+"위 : " + i.text+"\n")
        num += 1
