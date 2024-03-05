from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import openpyxl

import time
import random


# id, pw 입력

id = "****"
pw = "****"
id_css_tag = "body > div:nth-child(2) > div > form > div.input > input[type=text]:nth-child(1)"
pw_css_tag = "body > div:nth-child(2) > div > form > div.input > input[type=password]:nth-child(2)"
site_board_num = "389155"  #한밭대 자유게시판 사이트 번호


start_page = 1
pages_crawl = 1

exl_row = 2    # 처음 엑셀 row 값
exl_route = (r'C:\Users\admin\Desktop\Workspace\python\everytime crawling\everytime_crawling.xlsx')
exl = openpyxl.load_workbook(exl_route)
exl_ws = exl.active

# 함수들 

def input_text_to_textbox(text, css_selector):
    textbox = driver.find_element(By.CSS_SELECTOR, css_selector)
    textbox.click()
    textbox.send_keys(text)

def list_crawling(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    article = soup.find(class_="wrap articles")
    title = article.find_all("h2")
    content = article.find_all("p")
    comment = len(article.find_all(class_="comment"))
    url = article.find_all(href=True)
    no_comment = []

    data_tmp = []

    if(comment < len(title)):
        desc = article.find_all(class_="desc")
        for q in range(0, len(desc)):
            if(not(desc[q].find(class_="comment"))):
                no_comment.append(q)

    print(no_comment)

    for k in range(0,len(title)):
        if(k in no_comment):
            continue
        elif("?" in title[k].text):
            data_tmp.append("https://everytime.kr"+url[k]['href'])
        elif("?" in content[k].text):
            data_tmp.append("https://everytime.kr"+url[k]['href'])
    return data_tmp

def a_page_crawling(page_source):
    content_chkr = 0
    content = ""
    comments = ""

    soup = BeautifulSoup(page_source, "html.parser")
    article = soup.find(class_="wrap articles")
    title = article.find("h2")
    comment = article.find_all("p", class_ = "large")

    for i in comment:
        if content_chkr == 0:
            content_chkr = 1
            content = i.text
            continue
        comments = comments + i.text + "::"
    
    return title.text, content, comments
    

#크롬 드라이버 관련 설정 및 사이트 접속

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(5)
driver.maximize_window()
driver.get("https://account.everytime.kr/login")

# 로그인

# login_pg = driver.find_element(By.CSS_SELECTOR, "body > aside > div.login > a.button.login")
# login_pg.click()

input_text_to_textbox(id, id_css_tag)
input_text_to_textbox(pw, pw_css_tag)

time.sleep(random.random()+1)

driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div > form > input[type=submit]").click()

# 자유게시판 이동

d_url = []

for i in range(start_page, start_page + pages_crawl, 1):
    time.sleep(random.random()+1)
    driver.get(f"https://everytime.kr/{site_board_num}/p/{i}")

    time.sleep(random.random()+1)
    
    data_tmp = list_crawling(driver.page_source)
    for k in range(0, len(data_tmp), 1):
        d_url.append(data_tmp[k])


for k in d_url:
    time.sleep(random.random()+1)
    driver.get(k)

    time.sleep(random.random()+1)
    try:
        title, content, comments = a_page_crawling(driver.page_source)
    except:
        continue
    
    exl_ws[f'B{exl_row}'] = title
    exl_ws[f'C{exl_row}'] = content
    exl_ws[f'D{exl_row}'] = comments

    exl_row = exl_row + 1

    if exl_row % 100 == 0:
        time.sleep(random.random()+1)
        exl.save(exl_route)

    print(exl_row)

time.sleep(random.random()+1)
exl.save(exl_route)

