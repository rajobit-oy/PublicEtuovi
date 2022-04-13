from datetime import datetime
from robot.api import logger
import robot
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import robot.libraries.Screenshot as sc
from RPA.Desktop.Windows import Windows
#from RPA.Browser import Browser
from RPA.Browser.Selenium import Selenium

import time
from configs import OUTPUT_PATH

browser_lib = Selenium(auto_close=False)
browser_lib.auto_close=False
browser_lib.set_download_directory(OUTPUT_PATH,True)

from pprint import pprint
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from wantedValues import EtuoviData
from wantedValues import mappings
import pandas as pd
from retry import retry
import os
from selenium.webdriver.common.keys import Keys
import collections
def clickWithScript(xpath,browser_lib):
    for i in range(10):
        try:
            ele=browser_lib.find_element(xpath)
            browser_lib.driver.execute_script("arguments[0].click();",ele)
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            if(i==9):
                raise

import os
import datetime
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def downloadPDFFile(browser_lib):
    """Oletuksena että sivu on jo avattuna.
    Painaa PDF auki ja katsoo että tulee lataus kansioon.
    Tämä olettaa että PDF vieweriä ei käytetä vaan että lataus tulee suoraan download directoryyn!
    """
    names=browser_lib.get_window_names()
    n2=browser_lib.get_window_names()
    startClick=datetime.datetime.now()
    clickWithScript("//button[contains(@class,PrintPdfButton__printPdf__) and @rel='noopener nofollow']",browser_lib)
    for i in range(10):
        #browser_lib.click_button("//button[contains(@class,PrintPdfButton__printPdf__) and @rel='noopener nofollow']")
        afterNames=browser_lib.get_window_names()
        if(len(names)==len(afterNames)):
            print("sameNames")
            time.sleep(0.1*i)
            if(i==9):
                
                raise Exception("Pdf did not open after click")
        else:
            
            break
    from pathlib import Path
    for i in range(100):
        for path in Path(OUTPUT_PATH).rglob('*.pdf'):
            
            dt=modification_date(path)
            #print(f"{path} dt:{dt}")
            if(dt>startClick):
                print(f"found newer file:{path}")
                print("")
                browser_lib.switch_window("new")
                browser_lib.close_window()
                browser_lib.switch_window("main")
                return path
                
        time.sleep(0.1)
    #path=r"C:\asiakkaat\Libraries\RB.Netvisor.Activities\KirjanpidonRaportit\tuloslaskelma, kuukausittain.xaml"
    raise Exception("PDF ei saatu ladattua! Sitä ei koskaan tullut lataus kansioon")
    

if __name__ == "__main__":
    import Etuovi
    print("")
    import os
    full_path = os.path.realpath(__file__)
    print("in __main__:"+full_path + "\n")
    browser_lib.open_available_browser("https://www.etuovi.com/kohde/20715151")
    pdfPath=downloadPDFFile()
    import urllib.request
    #URL=browser_lib.driver.current_url
    ##URL=""
    #response = urllib.request.urlopen(URL)    
    #file = open("FILENAME.pdf", 'wb')
    #file.write(response.read())
    #file.close()
    browser_lib.click_button("id:icon")
    #if(set(n2)==set(names)):
    #    print("sameNames")
    browser_lib.find_elements("//button[contains(@class,PrintPdfButton__printPdf__)]")
    