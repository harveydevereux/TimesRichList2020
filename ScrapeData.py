from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from tqdm import tqdm
import pandas as pd

from numpy import ceil

# some library functions to work with the Times website
from header import *

import argparse

Headless=False
csv="TimesRichList2020.csv"

parser = argparse.ArgumentParser(description='parse filename output and headless mode option')
parser.add_argument('--headless', metavar='Headless', type=bool,
                    help='run in headless mode')
parser.add_argument('--csv', dest='csv', action='store_const',
                    const=csv, default="TimesRichList2020.csv",
                    help='name of csv to save to')

options = Options()
options.headless = Headless
driver = webdriver.Firefox(options=options)

driver.get("https://www.thetimes.co.uk/sunday-times-rich-list#TableFullRichList")

# get around the cookie consent
frame = WebDriverWait(driver, 20).until(
EC.presence_of_element_located((By.ID, "sp_message_iframe_140799")))

# click the I Agree button
driver.switch_to.frame(frame)

button = WaitForClickabilityXPATH(driver,'//button[text()="I Agree"]')
button.click()

# switch back to the default content after getting
# rid of the consent iframe
driver.switch_to.default_content()

CurrentMaxEntry = GetEntryEndNum(driver)
Data = pd.DataFrame()
print("Parsing Data")
pbar = tqdm(total = int(ceil(GetEntryMax(driver)/CurrentMaxEntry)))
while CurrentMaxEntry != GetEntryMax(driver):
    # while there are still table pages to see click on through!
    df = ParseTable(driver)
    Data = pd.concat([Data,df])
    button = WaitForClickabilityXPATH(driver,"//div[contains(text(),'Next')]")
    button.click()
    CurrentMaxEntry = GetEntryEndNum(driver)
    pbar.update(1)
# get final page
df = ParseTable(driver)
Data = pd.concat([Data,df])
pbar.update(1)
pbar.close()

driver.close()

Data.to_csv(csv)
