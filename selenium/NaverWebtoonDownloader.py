# -*- coding: utf-8 -*-
import os
import requests
from PIL import Image
from bs4 import BeautifulSoup
from itertools import count
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

class NaverWebtoonDownloader:
    # 웹툰고유번호, 다운로드 시작할 화, 자동멈춤, 셀레니움 사용여부 
    def __init__(self,title_id,start=1, stop_loop=False,use_selenium=False):
        self.title_id = title_id
        self.stop_loop = stop_loop
        self.use_selenium = use_selenium
        self.start = start

        # costomized Header
        self.headers = {'Referer': 'http://comic.naver.com/index.nhn'}
        # background color for png file
        self.WHITE = (255, 255, 255)
        # URL for NAVER webtoon
        self.url = 'http://comic.naver.com/webtoon/detail.nhn'
        self.ep_list = []
        if(use_selenium):
            self.usingSelenium()
        else:
            self.download()


    def getTitle(self,no,html=None):
        # webtoon title & episode title
        if(self.use_selenium):
            self.soup = BeautifulSoup(html, 'html.parser')
        else:
            self.params = {'titleId': self.title_id, 'no': no}
            self.html = requests.get(self.url, params=self.params).text
            self.soup = BeautifulSoup(self.html, 'html.parser')  # requests로 가져온 웹페이지를 파싱함
        wt_title = self.soup.select('.detail h2')[0].text
        ep_title = self.soup.select('.tit_area h3')[0].text
        wt_title = wt_title.split()[0]
        wt_title = wt_title.replace(':', '')
        ep_title = ' '.join(ep_title.split()).replace('?', '')
        return wt_title,ep_title


    def getImage(self,wt_title):
        # episode images
        img_path_list = []
        
        #리스트 내포. tag속성이 'src'인 친구들 중 wt_viewer클래스의 img 자식 속성 긁어모으기  
        img_list = [tag['src'] for tag in self.soup.select('.wt_viewer > img')]
        for img in img_list:

            # save the images
            self.img_name = os.path.basename(img)
            self.img_path = os.path.join(wt_title, self.img_name)

            self.dir_path = os.path.dirname(self.img_path)
            if not os.path.exists(self.dir_path):
                os.makedirs(self.dir_path)

            img_path_list.append(self.img_path)

            if os.path.exists(self.img_path):
                continue

            img_data = requests.get(img, headers=self.headers).content
            with open(self.img_path, 'wb') as f:
                f.write(img_data)

        self.im_list = []
        for img_path in img_path_list:
            im = Image.open(img_path)
            self.im_list.append(im)
        return self.dir_path,img_path_list


    def saveImage(self,dir_path,img_path_list,ep_title):
        # make canvas for appending images
        canvas_size = (
            max(im.width for im in self.im_list),
            sum(im.height for im in self.im_list)
        )
        canvas = Image.new('RGB', canvas_size)
        top = 0
        # save the webtoon
        for im in self.im_list:
            canvas.paste(im, (0, top))
            top += im.height
        canvas.save("./"+self.dir_path + '/' + ep_title + '.png')

        # delete all temporally images for webtoon
        time.sleep(0.5)
        for img_path in img_path_list:
            if(img_path.find("blank") == -1):
                os.remove(img_path)
            else:
                pass


    def download(self):
        for no in count(self.start): #1부터 무한대로 올라감
            wt_title, ep_title = self.getTitle(no)
            # check if this episode is last or not
            if(self.stop_loop):
                #off_now
                if ep_title in self.ep_list:
                    break
            self.ep_list.append(ep_title)
            dir_path, img_path_list = self.getImage(wt_title)
            self.saveImage(dir_path, img_path_list, ep_title)
            print(wt_title + ' ' + ep_title + ' is downloaded.')
        print('All episode is downloaded completely.')


    def usingSelenium(self):
        chrome_version = "81"
        id = "아이디"
        pw = "비밀번호"
        path = ".\chromedriver_win32_v" + chrome_version + "\chromedriver.exe"

        self.driver = webdriver.Chrome(path)
        # 웹페이지 로딩까지 기다릴 시간(초). 너무 빠르면 못찾을때도 있음.
        self.driver.implicitly_wait(30)
        self.driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

        self.copy_input('//*[@id="id"]', id)
        time.sleep(1)
        self.copy_input('//*[@id="pw"]', pw)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

        #target = self.driver.find_element_by_css_selector("#PM_ID_ct > div.header > div.special_bg > div > div.area_logo > h1 > a")


        for no in count(self.start): #1부터 무한대로 올라감
            # 웹툰 들어가기
            make_url = urljoin(self.url, "?titleId=" + str(self.title_id) + "&no=" + str(no))
            print("make_url : "+make_url)

            self.driver.get(make_url)
            html = self.driver.page_source
            wt_title, ep_title = self.getTitle(no,html)
            # check if this episode is last or not
            if(self.stop_loop):
                #off_now
                if ep_title in self.ep_list:
                    break
            self.ep_list.append(ep_title)
            dir_path, img_path_list = self.getImage(wt_title)
            self.saveImage(dir_path, img_path_list, ep_title)
            print(wt_title + ' ' + ep_title + ' is downloaded.')
        print('All episode is downloaded completely.')

    # 클립보드에 input을 복사한 뒤
    # 해당 내용을 actionChain을 이용해 로그인 폼에 붙여넣기
    def copy_input(self,xpath, input):
        pyperclip.copy(input)
        self.driver.find_element_by_xpath(xpath).click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(1)

if __name__ == '__main__':
    number = input("웹툰 고유번호 6자리를 입력하세요 : ")
    downloader = NaverWebtoonDownloader(int(number),start = 1,stop_loop=False,use_selenium=False)
