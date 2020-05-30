from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import pandas as pd

def GetEntryEndNum(driver):
    '''
    This finds the div which stores the Wealth position of the last person in the table.
    '''
    nav = driver.find_element_by_xpath("//div[@class='NavigationMessage']")
    return int(nav.text.split(" ")[3].replace(",",""))

def GetEntryStartNum(driver):
    '''
    This finds the div which stores the Wealth position of the first person in the table.
    '''
    nav = driver.find_element_by_xpath("//div[@class='NavigationMessage']")
    return int(nav.text.split(" ")[1].replace(",",""))

def GetEntryMax(driver):
    '''
    This finds the max number of table rows, so we know how many to click through
    '''
    nav = driver.find_element_by_xpath("//div[@class='NavigationMessage']")
    return int(nav.text.split(" ")[5].replace(",",""))

def RowsInPage(driver):
    # plus one as format is row from x to y inclueding x and y
    return GetEntryEndNum(driver)-GetEntryStartNum(driver)+1

def WaitForClickabilityXPATH(driver,xpath):
    '''
    tells selenium to wait until the element with the XPATH xpath is clickable and then returns it
    '''
    element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, xpath)))
    return element

def ParseNumbers(x):
    '''
    meta-code to parse strings like "16bn" -> 16000000000.0
    '''
    y = x.replace(" ","")
    try:
        if ("m" in y):
            return eval(y.replace("m","*1e6"))
        elif ("bn" in y):
            return eval(y.replace("bn","*1e9"))
    except:
        print("Error: ParseNumbers")

def ParseTable(driver):
    '''
    This is fairly hard coded to extract the data from the Sunday Times Rich List
    2020 page: https://www.thetimes.co.uk/sunday-times-rich-list

    worked on 30th May 2020
    '''
    colnames = ['Rank', 'Name', 'Worth', 'Rise/Fall', 'Source of wealth']
    df = pd.DataFrame(columns=colnames)
    # the data is stored in a div called TableFullRichList
    frame = driver.find_element_by_id("TableFullRichList")
    # gets all the rows in the table
    # the are 2 rows for the column names and a key to the data
    rows = frame.find_elements_by_tag_name("tr")
    for i in range(2,RowsInPage(driver)+2):
        position = rank = i - 2 + GetEntryStartNum(driver)
        # get rid of "="
        r = rows[i].text.replace("=","")
        if ")" in rows[i].text:
            rank = r.split("(")[0]
            # previously seen (i.e last year)
            name = r.split(")")[1].split("£")[0]
            if r.count("£") == 1:
                # no change this year
                worth = r.split(")")[1].split("£")[1].split(" No change")[0]
                change = 0
                sector = r.split(")")[1].split("£")[1].split("No change ")[-1]
            else:
                # change this year
                worth = r.split(")")[1].split("£")[1]
                sector = " ".join(r.split(")")[1].split("£")[2].split(" ")[1:])
                change = r.split(")")[1].split("£")[2].split(" ")[0]
                change = ParseNumbers(change)
        else:
            # new entry
            rank = r.split(" ")[0]
            name = " ".join(r.split("£")[0].split(" ")[1:])
            worth = r.split("£")[1].split(" ")[0]
            change = "New"
            sector = r.split("New entry ")[-1]

        worth = ParseNumbers(worth)
        df.loc[position,:] = [rank,name,worth,change,sector]
    return df
