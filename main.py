from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import numpy as np

def delay ():
    time.sleep(3)

#options = Options()

#options.add_argument("--headless")

path = os.getcwd() + "\\tmp\\"

#driver = webdriver.Chrome()
driver = webdriver.Firefox()

#params = {"behavior": "allow", "downloadPath": path}
#driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

baseLink = "https://nfg.sefaz.rs.gov.br/cadastro/ConsultaDocumentos.aspx"

driver.get(baseLink)

cpf = "your cpf"
driver.find_element_by_name("nro_cpf_loginNfg").send_keys(cpf)

cod = "your password"
driver.find_element_by_name("senha_loginNfg").send_keys(cod)

frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])

delay()

try:
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()

    delay()

    driver.switch_to.default_content()

    driver.find_element_by_class_name("botaoLoginNfg").click()
except:
    print("Falhou no Captcha")
    exit(1)

driver.execute_script('document.getElementById("txtDtInicial").value = "01012022"')

driver.execute_script('document.getElementById("txtDtFinal").value = "17052022"')

delay()

driver.find_element_by_class_name("botaoAzul").click()

i = 1
page = 1
pageAnt = 0

links = [""]

while page != pageAnt:
    delay()

    numRows = len(driver.find_elements_by_xpath("//table[@id='areaDocumentoTab']/tbody/tr"))

    i = 1

    while i <= numRows:
        xpath = "//table[@id='areaDocumentoTab']/tbody/tr[" + str(i) + "]/td[7]/a"
        link = driver.find_element_by_xpath(xpath).get_attribute("href")
        if i == 1 and page == 1:
            links[0] = link
        links.append(link)
        i += 1

    pageAnt = page

    driver.find_element_by_id("areaDocumentoTab_next").click()

    page = int(driver.find_element_by_xpath("//a[@class='paginate_button current']").text)

    print(page)

for link in links:

    driver.get(link)

    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])

    delay()

    driver.find_element_by_xpath("//input[@class='button']").click()

    f = csv.writer(open('produtos.csv', 'w'))

    pages = []

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    all_tables = soup.find_all('td', {'class': 'NFCDetalhe_Item'})
    #tbody = all_tables.find_all('td')

    with open('produtos.csv', mode='w') as produtos:
        for item in all_tables:
            escrivao = csv.writer(produtos)
            escrivao.writerow([item.text])

    for item in all_tables:
        print(item.text)
        f.writerow(item.text)

    driver.switch_to.default_content()

driver.get(baseLink)

#driver.find_element_by_xpath("//button[@class='dt-button buttons-csv buttons-html5']").click()
