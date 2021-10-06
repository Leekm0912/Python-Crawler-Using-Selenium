## **사용법**

### **1. 크롬 버젼에 맞는 드라이버를 다운받기**

버젼확인방법우측상단 ... 클릭 -> 도움말 -> Chrome정보

크롬 드라이버 다운로드[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

### **2. config.ini 파일 수정**

config.ini 파일을 열어 파라미터를 수정해 사용하시면 됩니다! (주석 참고)

```
[DEFAULT]
# 검색어 입력
# 이후 검색어 명으로 폴더 생성
SEARCH = 동양인 눈

# 이미지파일 저장 경로 (마지막 / 제외하고)
# ex)./downloads
SAVA_PATH = ./downloads

# 크롬 드라이버 경로 설정(마지막 / 제외하고)
# ex) ./chromedriver_win32_v87
CHROME_DRIVER_PATH = ./chromedriver_win32_v87

# 구글 이미지 클래스명 넣어주기.
GOOGLE_IMG_CLASSNAME = .rg_i.Q4LuWd
```

---

## **3rd party Library**

- urllib
    
    ⇒ url 경로 완성과 이미지 다운로드를 위해 사용
    
- bs4
    
    ⇒ html 요소 파싱을 위해 사용
    
- selenium
    
    ⇒ 웹 자동화 관련 라이브러리
