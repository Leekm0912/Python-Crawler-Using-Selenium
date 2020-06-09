# -*- coding: utf-8 -*-
from os import path,remove,system
from sys import exit
from ctypes import windll
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pandas import DataFrame as DF
from webbrowser import open as open_br
import datetime

STD_INPUT_HANDLE   = -10
STD_OUTPUT_HANDLE  = -11
STD_ERROR_HANDLE   = -12

FOREGROUND_YELLOW     = 0x06
FOREGROUND_BLUE      = 0xB1 # text color contains blue.
FOREGROUND_GREEN     = 0x02 # text color contains green.
FOREGROUND_RED       = 0x04 # text color contains red.
FOREGROUND_WHITE       = 0x07 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
BACKGROUND_BLUE      = 0x10 # background color contains blue.
BACKGROUND_GREEN     = 0x20 # background color contains green.
BACKGROUND_RED       = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

std_out_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    bool = windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool

class SchoolCrawler:
    def __init__(self,notice_url,save=False):
        print("로딩중")
        self.save = save
        self.notice_url = notice_url
        self.data = []
        self.date = []
        self.now = datetime.datetime.now()
        self.day = self.now.strftime('%Y.%m.%d')
        # day test
        #self.day = "2020.06.03"
        self.return_code = False


    def getNotice(self):
        for i in range(len(notice_url)):
            self.html = get(self.notice_url[i][1]).text
            self.soup = BeautifulSoup(self.html, 'html.parser')

            for href in self.soup.find_all("td",class_ = '_artclTdTitle'):
                temp = []
                make_url = urljoin(self.notice_url[i][1], href.find("a")["href"])
                temp.append(href.find("strong").text)
                temp.append(make_url)
                self.data.append(temp)
            for day in self.soup.find_all("td",class_ = '_artclTdRdate'):
                self.date.append(day.text)



    def saveNoticeToCSV(self):
        result = DF(self.data)
        result.columns = ['title','url']
        file = '학교_학과_공지사항.csv'
        if path.isfile(file):
            remove(file)
        result.to_csv(file,encoding='cp949')


    def getTitle(self):
        no = 1
        title_no = 0
        set_color(FOREGROUND_GREEN)
        print("Create by 이경민")
        set_color(FOREGROUND_WHITE)
        if(self.return_code == 2):
            self.now = datetime.datetime().now()
            self.day = self.now.strftime('%Y.%m.%d')

        print(self.now.strftime('%Y-%m-%d %H:%M:%S')+" 기준")
        for i in self.data:
            if(no % 10 == 1):
                set_color(FOREGROUND_WHITE)
                print("\n=================="+self.notice_url[title_no][0]+"==================")
                title_no+=1
            if(self.date[no-1] == self.day):
                # 오늘 업데이트 된 공지는 노란색으로
                set_color(FOREGROUND_YELLOW)
            else:
                set_color(FOREGROUND_WHITE)
            # 출력되는 리스트
            #if(i[0].find("장학") != -1):
            #    set_color(FOREGROUND_RED)
            print(no," : "+i[0]+" | "+self.date[no-1]+" 등록")
            no+=1


    def start(self):
        if(self.save):
            self.saveNoticeToCSV()
        system("cls")
        self.getTitle()
        no = input("\n이동하실 번호를 입력해 주세요(종료:0)\n새로고침하려면 r을 입력하세요\n입력:")
        if(no == 'r' or no == 'R'):
            system("cls")
            print("로딩중")
            self.return_code = 2
            self.refresh()
        else:
            try:
                no = int(no)
            except:
                self.return_code = 0
                self.start()
            if (not (1 <= no <= len(self.notice_url)*10)):

                if(no == 0):
                    exit()
            else:
                open_br(self.data[no-1][1])
            self.return_code = 1
            self.start()
        return self.return_code


    def refresh(self):
        self.data = []
        self.getNotice()
        if(self.save):
            self.saveNoticeToCSV()
        self.start()


if __name__ == '__main__':
    notice_url = []
    with open("list.txt", "r", encoding="utf-8") as r:
        temp = r.readlines()
    for url in temp:
        notice_url.append(url.replace("\n","").split("="))
    s = SchoolCrawler(notice_url)
    s.getNotice()
    s.start()
