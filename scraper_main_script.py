from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import pandas as pd
from tqdm import tqdm

url = "https://www.stfrancismedicalcenter.com/find-a-provider/"

full_name_ls = []
speciality_ls = []
added_speciality_ls = []
full_address_ls = []
practice_ls = []
address_ls = []
state_ls = []
zip_ls = []
phone_ls = []
error_ls = []

def make_excel():
    data = {'Full Name':full_name_ls,
            'Specialty':speciality_ls,
            'Add Specialty':added_speciality_ls,
            'Full Address' : full_address_ls,
            'Practice': practice_ls,
            'Address':address_ls,
            'State':state_ls,
            'Zip' : zip_ls,
            'Phone':phone_ls,
    }
    df = pd.DataFrame(data)
    df.to_excel("assignment.xlsx")

def scrape(doc_soup):
    flag=True
    soup_main = doc_soup.find_all('div',{"class":"LocationEHP__Wrapper-sc-1y4lei3-0 kPUlFg"})
    doctor_name = doc_soup.find('h3')
    doctor_speciality_ls = doc_soup.find_all('div',{"class":"ProviderMainCard__Tag-lt2r6j-1 dmNAGQ speciality-tag"})
    doctor_speciality = doctor_speciality_ls[0]
    doctor_speciality = doctor_speciality.text
    full_name_ls.append(doctor_name.text)
    try:
        a,b = doctor_speciality.split(",")
        speciality_ls.append(a)
        added_speciality_ls.append(b)
    except:
        speciality_ls.append(doctor_speciality)
        added_speciality_ls.append("--")
        
    for i in soup_main:
        a = i.find_all('div',{"class":"BasicInfo__Wrapper-gas5ca-0 hMRnVk education-title basicInfoWrapper"})
        b = i.find_all('div',{"class":"BasicInfo__Wrapper-gas5ca-0 hMRnVk basicInfoWrapper"})
        try:
            practice = a[0].text
            address_main = b[0].text
            phone_main = b[2].text
        except:
            flag=False
            practice_ls.append("--")
            full_address_ls.append("--")
            address_ls.append("--")
            phone_ls.append("--")
            state_ls.append("--")
            zip_ls.append("--")
    if flag:
        practice_ls.append(practice)
        full_address_ls.append(practice+" ; "+address_main)
        address_ls.append(address_main)
        phone_ls.append(phone_main)
        state_ls.append(address_main[-8:-6])
        zip_ls.append(address_main[-5:-1])
        

def main():
    driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe') 
    driver.get(url) 
    time.sleep(5) 
    div_const = 1
    for i in tqdm (range(15), desc="Loading..."):
        if div_const>10:
            for j in range(int(div_const/10)):
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        try:
            driver.find_element("xpath",f'(//button[@class="CustomButton-j1wfwm-0 bfxmwP outlined"])[{div_const}]').click()
            time.sleep(4)
            html = driver.page_source
            webpage_soup = soup(html,'html.parser')
            scrape(webpage_soup)
            driver.find_element("xpath","(//*[name()='svg'])").click()
        except:
            print(f"Error Occured At Div {div_const}")
            error_ls.append(div_const)
            time.sleep(2)
            driver.get(url)
        div_const+=1

if __name__=="__main__":
    main()
    make_excel()
