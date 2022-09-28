from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from PIL import Image, ImageOps
import cv2
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
from time import sleep
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

driver = webdriver.Firefox(executable_path=r"C:\browserDrivers\geckodriver.exe")
driver.get("https://esearch.delhigovt.nic.in/Complete_search.aspx")

def get_captcha_text():
    captcha_url = driver.find_element(By.XPATH, "//div[@id='ctl00_ContentPlaceHolder1_UpdatePanel4']/div[1]/img[1]").get_attribute("src")
    urllib.request.urlretrieve(captcha_url, "captcha.jpg")
    img = cv2.imread("captcha.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img = cv2.medianBlur(img, 3)
    cv2.imwrite("image_name.jpg", img)
    img = Image.open("image_name.jpg")
    captcha_text = pytesseract.image_to_string(img) 
    captcha_text = captcha_text.replace(" ", "").strip()
    print(captcha_text)



Select(driver.find_element( By.ID, "ctl00_ContentPlaceHolder1_ddl_sro_s")).select_by_visible_text("Central -Asaf Ali (SR III)")
sleep(1)
Select(driver.find_element( By.ID, "ctl00_ContentPlaceHolder1_ddl_loc_s")).select_by_visible_text("Ajmal Khan Road")
Select(driver.find_element( By.ID, "ctl00_ContentPlaceHolder1_ddl_year_s")).select_by_visible_text("2021-2022")
# get_captcha_text()
sleep(7)
driver.find_element( By.ID, "ctl00_ContentPlaceHolder1_btn_search_s").click()

df = pd.DataFrame()
tot_pages = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_gv_search_ctl13_lblTotalNumberOfPages").get_attribute('innerHTML')
tot_pages = int(tot_pages)
cur_page = 1

while cur_page <= tot_pages:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    tables = soup.find_all('table')
    df_temp = pd.read_html(str(tables))[0]
    df_temp.drop(df.tail(1).index,inplace = True)
    df = pd.concat([df, df_temp])
    cur_page = cur_page + 1
    if cur_page != tot_pages:
        sleep(1)
        element = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_gv_search_ctl13_Button2")
        driver.execute_script("arguments[0].click();", element)
        sleep(5)

df = df.dropna(how='any',axis=0) 
df.to_csv("sample.csv", index=False)
print(df)

