from datetime import datetime
from robot.api import logger
import robot
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

import robot.libraries.Screenshot as sc
from RPA.Desktop.Windows import Windows
from RPA.Browser import Browser
from RPA.Browser.Selenium import Selenium
Selenium.auto_close=False
import time
import shutil
import handlePDFDownload
from configs import OUTPUT_PATH,WORKITEMS
browser_lib = Selenium(auto_close=False)
browser_lib.set_download_directory(OUTPUT_PATH,True)
browser_lib.auto_close=False
from pprint import pprint
def example3(expected_data):
    logger.info("example3!")
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from wantedValues import EtuoviData
from wantedValues import mappings
import pandas as pd
from retry import retry
import os
from selenium.webdriver.common.keys import Keys


import robocorpapi
import pythonSheet
import traceback

from RPA.Robocorp.WorkItems import WorkItems 
WORKITEMS=WorkItems()


def printToOutput(toWRite:str):
    print(toWRite)
    with open(os.path.join(OUTPUT_PATH,"omaLog.txt"), "a+",encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%H:%M:%S %d.%m')}    {toWRite}\n")

    

def getAttributes(element):
    attrs = browser_lib.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    pprint(attrs)

def oikotieVersio():
    #start chrome.exe -remote-debugging-port=9222
    oikotieUlr="https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100"
    #url jos halutaan pelkkä pirkanmaa+ei uudiskohteita
    oikotieUlr="https://asunnot.oikotie.fi/myytavat-asunnot?pagination=1&locations=%5B%5B7,7,%22Pirkanmaa%22%5D%5D&cardType=100&newDevelopment=0"
    #https://robocorp.com/docs/development-guide/browser/how-to-attach-to-running-chrome-browser
    browser_lib.attach_chrome_browser(port=9222)
    browser_lib.go_to(oikotieUlr)
    #browser_lib.open_available_browser("https://asunnot.oikotie.fi/myytavat-asunnot?cardType=100")
    #Etsitään iframea, jos se tulee laitetaan se pois
    try:
        iframeElement=browser_lib.wait_until_page_contains_element("//iframe[@title='SP Consent Message']",timeout=1)
        browser_lib.select_frame("//iframe[@title='SP Consent Message']")
        browser_lib.click_button("//button[@title='Hyväksy kaikki evästeet']")
        browser_lib.unselect_frame()
    except AssertionError as assE:
        if("//iframe[@title='SP Consent Message']" not in str(assE)):
            raise
    #//button[@analytics-click='search_click_pagination']/span[text()='Seuraava']
    nextEle=browser_lib.find_element("//button[@analytics-click='search_click_pagination']/span[text()='Seuraava']/..")
    getAttributes(nextEle)
    printToOutput(nextEle.get_attribute("disabled"))
    if(nextEle.get_attribute("disabled")=="disabled"):
        printToOutput("no more next")
    #browser_lib.find_elements("//a[contains(@href,'tampere')]")
    cardElements=browser_lib.find_elements("//div[@class='cards']//a[contains(@href,'myytavat-asunnot')]")
    allHrefs=[hele.get_attribute("href") for hele in cardElements]
    printToOutput(allHrefs)
    #Looppaa kaikki next sivut ja kerää hrefit!


def clickWithScript(xpath):
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

def checkboxAndVerify(selector,tryTimes=10):
    """
    Helper function to get checkbox selected.
    Clicks checkbox with script and checks that it got selected.
    """
    for i in range(tryTimes):
        try:
            
            clickWithScript(selector)
            #browser_lib.find_element(selector).click()#select_checkbox(selector)
            browser_lib.checkbox_should_be_selected(selector)
            #print(selector)
            getAttributes(browser_lib.find_element(selector))
            break
        except Exception as e:
            time.sleep(0.1*tryTimes)
            #browser_lib.scroll_element_into_view()
            if(i==tryTimes-1):
                raise
        



@retry(tries=10,delay=0.1, backoff=2, max_delay=2)
def getCompactInfos():
    infos=browser_lib.find_elements("//div[contains(@class,'CompactInfoRow__infoRow')]")
    texts=[info.text for info in infos]
    textDicts={}
    for t in texts:
        splittedV=t.split("\n")
        #sijainnissa pitää ottaa koko rivi (monen \n mukaan)
        if("Sijainti"==splittedV[0]):
            textDicts[splittedV[0]]=" ".join(splittedV[1:])
            try:
                textDicts[splittedV[0]]=splittedV[2]  #Jos halutaan loppu osa esim "tampere keskusta"+", "+splittedV[1]
            except Exception as e:
                printToOutput(e)
        else:
            textDicts[splittedV[0]]=splittedV[1]
    #pprint(texts)
    return textDicts

#Minne tallennetaan








class Etuovi:
    """Give this library a proper name and document it."""
    def setWorkItems(self,newWorkItem):
        global WORKITEMS
        WORKITEMS=newWorkItem
        print(newWorkItem)
        print("")
    def example2_python_keyword(self,expected_data=""):
        logger.info("example2!")
    def example_python_keyword(self):
        path=sc.Screenshot().take_screenshot()
        logger.info(path)
        logger.info("This is Python!")
        logger.info("Lisää äöäöäöä!")
        self.example2_python_keyword("hahaa")
        example3("sada")
        BuiltIn().run_keyword(name="Example keyword3")
        #TÄmä tekee logi merkinnän
        BuiltIn().run_keyword(name="MyLibrary.Example2 Python Keyword")
        #Tämä ei tee logi merkintää
        BuiltIn().call_method(object=self,method_name="example2_python_keyword")
    def keyword(self,log_level="INFO"):
        """Does something and logs the output using the given level.


        Valid values for log level` are "INFO" (default) "DEBUG" and "TRACE".

        See also `Another Keyword`.
        """
        # ...
        logger.info("keywordiiiii")

    def another_keyword(self,argument, log_level="INFO"):
        """Does something with the given argument else and logs the output.

        See `Keyword` for information about valid log levels.
        """
        logger.info("another_keyword")

    def navigateToSearch(self):
        browser_lib.open_available_browser("https://www.etuovi.com/haku/myytavat-asunnot",headless=True)
        etuovi="https://www.etuovi.com/haku/myytavat-asunnot"

        browser_lib.go_to(etuovi)
        try:
            popUp=browser_lib.wait_until_page_contains_element("id:almacmp-modal-layer1",timeout=1)
            popUp=browser_lib.find_element("id:almacmp-modal-layer1")
            #browser_lib.select_frame("//iframe[@title='SP Consent Message']")
            browser_lib.click_button(popUp.find_element_by_xpath("//button[contains(text(),'Hyväksy')]"))#"//button[@title='Hyväksy kaikki evästeet']")
            #browser_lib.unselect_frame()
        except AssertionError as assE:
            if("almacmp-modal-layer1" not in str(assE)):
                raise

    def exceptionWorkItemLogging(self):
        try:
            printToOutput("taking screenshot and adding it to workitem")
            browser_lib.capture_page_screenshot("EMBED")
            WORKITEMS.set_work_item_variable("Failed",True)
            #Testin vuoksi otetaan myös outputhiin file
            savedScreenshot=browser_lib.capture_page_screenshot("errorScreenshot_{index}.png") 
            WORKITEMS.add_work_item_file(savedScreenshot)
            WORKITEMS.save_work_item()
            printToOutput("work item saved and screenshotted")
        except Exception as e:
            printToOutput("exception work item saving \n "+traceback.format_exc())
            printToOutput(str(e))
    def exceptionRestart(self):
        """close browser
        """
        browser_lib.close_browser()


    def handlePage(self,url) ->dict:
        try:
            print(f"Handling page {url}")
            browser_lib.go_to(url)
            #Haetaan Compactit infot
            textDicts=getCompactInfos()
            
            if(textDicts["Kohdenumero"] not in url):
                raise Exception(f"Kohdenumero {textDicts['Kohdenumero']} ei täsmää urliin {url}")
            kohdeDir=os.path.join(OUTPUT_PATH,textDicts["Kohdenumero"])
            try:
                os.mkdir(kohdeDir)
            except FileExistsError as e:
                pass
            with open(os.path.join(kohdeDir,"pageTexts.json"), "w+",encoding="utf-8") as file:
                json.dump(textDicts,file, sort_keys=True, indent=4, separators=(",", ": "))
            #wantedDatas:EtuoviData=EtuoviData(**textDicts)
            newDict={}
            for key,value in mappings.items():
                if(value in textDicts.keys()):
                    #print("found ")
                    newDict[key]=textDicts[value]
                else:
                    newDict[key]=value
            newDict["Tyyppi"]+=" | "+textDicts["Huoneistoselitelmä"]
            newDict["PVM"]=datetime.now().strftime("%d/%m/%y")
            newDict["PVM_Vanhahinta"]=datetime.now().strftime("%d/%m/%y")
            newDict["Linkki"]=f"https://www.etuovi.com/kohde/{newDict['KohdeNumero']}"
            #Haetaan myyjä ja firma
            firmae=browser_lib.find_element("//div[@id='contact']//*[@my='1'] | //*[contains(@class,'PrivateSellerLogo__Container')] | //*[contains(@class,'OfficeContainer__officeName')]")
            #jos normi           "//div[@id='contact']//*[@my='1']")
            #jos private seller: "//*[contains(@class,'PrivateSellerLogo__Container')]")
            firma=firmae.text
            try:
                myyjänimi=browser_lib.find_element("//div[@id='contact']//*[@mb='1']").text
            except Exception as e:
                printToOutput(e)
                myyjänimi=str(e)
            newDict["Firma"]=firma
            newDict["Myyjänimi"]=myyjänimi

            #printToOutput("")
            #printToOutput("")
            try:
                file=handlePDFDownload.downloadPDFFile(browser_lib=browser_lib)
                result_path=os.path.join(kohdeDir,"esite.pdf")
                printToOutput(f"got file {file} moving it to {result_path}")
                for i in range(100):
                    try:
                        shutil.move(file,result_path)
                        printToOutput(f"got file {file} moved to {result_path}")
                        break
                    except PermissionError as e:
                        if(i>98):
                            raise
                newDict["LocalFile"]=result_path
                newDict["pdfSuccess"]=True
            except Exception as e:
                printToOutput("exception on downloading file \n "+traceback.format_exc())
                printToOutput(" exception:"+str(e))
                browser_lib.capture_page_screenshot("EMBED")
                newDict["LocalFile"]=str(e)
                newDict["pdfSuccess"]=False
                
                    
            with open(os.path.join(kohdeDir,"result.json"), "w+",encoding="utf-8") as file:
                json.dump(newDict,file, sort_keys=True, indent=4, separators=(",", ": "))
            
            if(newDict["pdfSuccess"]):
                printToOutput("esite got downloaded, starting to send it and updating sheet!")
                newSheet=pythonSheet.pythonSheet()
                newSheet.addEsite(newDict)
            else:
                printToOutput("PDF failed, raising bussiness exception!")
                printToOutput("Clsign browser!")
                #browser_lib.close_browser()
                #time.sleep(2)

                raise Exception("BUSINESS, ei saatu esitettä ladattua")
        except Exception as e:
            emsg="Exception inside handle page: \n "+traceback.format_exc()
            printToOutput(emsg)
            WORKITEMS.set_work_item_variable("Failed",True)
            WORKITEMS.set_work_item_variable("Message",emsg)
            raise
        return newDict


    def CreateWorkItemsEiLogi(self):
        workItems=WorkItems()
        browser_lib.open_available_browser("https://www.etuovi.com/haku/myytavat-asunnot")
        self.navigateToSearch()
        self.doSearch()
        allfFoundHrefs=self.getAllHrefs()
        for item in allfFoundHrefs:
            workItems.create_output_work_item(variables=item,save=True)

    def CreateWorkItems(self):
        """
        Navigates to Etuovi, gives wanted search parameters
        Finds all Hrefs and creates worker items based on them
        """
        
        
        curdir = BuiltIn().get_variable_value("${CURDIR}")
        printToOutput(curdir)
        vars=BuiltIn().log_variables()
        workItems=WorkItems(autoload=True)
        workItems.get_input_work_item()
        #Calling this via BuiltIn to get Loggin, is there easier ways to achieve this?
        BuiltIn().run_keyword(name="Etuovi.NavigateToSearch")
        #self.navigateToSearch()
        self.doSearch()
        allfFoundHrefs=BuiltIn().run_keyword(name="Etuovi.GetAllHrefs")
        #Make worker items, if they are not created or handled already
        for index,item in enumerate(allfFoundHrefs):
            printToOutput(f"creating item index:{index}.")
            printToOutput(f"checking if item is already handled")
            id=item.split("/")[-1]
            existsAlready=BuiltIn().run_keyword("robocorpapi.Item With Key Exists",id)
            if(not existsAlready):
                workItems.create_output_work_item(variables={"id":id,"href":item},save=True)
            else:
                printToOutput("Do not make new, because it already exists in worker items")

    def doSearch(self,within7days=True):
        """
        Navigates to search if needed and gives wanted search values
        """
        try:
            browser_lib.find_element("//input[@placeholder='Sijainti tai kohdenumero']")
        except Exception as e:
            self.navigateToSearch()
        #set pirkanmaa and check that it is actally selected!
        browser_lib.input_text("//input[@placeholder='Sijainti tai kohdenumero']","Pirkanmaa")
        browser_lib.find_element("//input[@placeholder='Sijainti tai kohdenumero']").send_keys(Keys.RETURN)
        #This was not as stable as send_keys
        #browser_lib.press_keys("//input[@placeholder='Sijainti tai kohdenumero']",keys="RETURN")
        #when pirkanmaa is added this element should be found!
        browser_lib.wait_until_page_contains_element("//span[@class='MuiChip-label' and text()='Pirkanmaa']")

        checkboxAndVerify("//input[@name='OWN']")
        checkboxAndVerify("name:PARTIAL_OWNERSHIP")
        
        printToOutput("")
        for i in range(10):
            try:
                clickWithScript("//input[@value='NO_NEW_BUILDINGS']")
                break
            except Exception as e:
                printToOutput(e)
                time.sleep(1)
                if(i==9):
                    raise
        if(within7days):
            clickWithScript("//input[@value='WITHIN_SEVEN_DAYS']")
        
        browser_lib.click_button("id:searchButton")
        #When search is done, this element should be found!
        browser_lib.wait_until_page_contains_element("id:paginationNext")

    def getAllHrefs(self):
        """Gets Hrefs of all card elements,
        from this we get url of worker items
        """
        allFoundHrefs=[]
        results=[]
        oldElements=[]
        for i in range(1000):
            result={}
            #readyState=browser_lib.driver.execute_script("return document.readyState")
            #printToOutput(readyState)
            for j in range(30):
                try:
                    cardElements=browser_lib.find_elements("//div[@id='announcement-list']//a[contains(@href,'kohde/')]")
                    allHrefs=[hele.get_attribute("href").split("?haku")[0] for hele in cardElements]
                    break
                #When the page is not loaded, staleElementReference is thrown because we got old elements.
                except StaleElementReferenceException as e:
                    printToOutput(e)
                    if(i==29):
                        raise
            
            result[i]=allHrefs
            allFoundHrefs+=allHrefs
            results.append(result)
            browser_lib.wait_until_page_contains_element("id:paginationNext")
            #Next button becomes disabled when we have reached end of the search
            disabledState=browser_lib.find_element("id:paginationNext").get_attribute("disabled")
            if(disabledState):
                if("true" in disabledState):
                    printToOutput("next is disabled, stopping!")
                    break
            browser_lib.click_button("id:paginationNext")
            oldElements=cardElements
        #with open("tulokset.json", "w+",encoding="utf-8") as file:
        #    json.dump(results,file, sort_keys=True, indent=4, separators=(",", ": "))
        return allFoundHrefs



if __name__ == "__main__":
    
    #from RPA.HTTP import HTTP 
    #newHTTP=HTTP()
    #newHTTP.download("https://www.etuovi.com/fcfafa32-7634-43a5-b730-361bf07c0b35")
    #browser_lib.attach_chrome_browser(port=9222)
    printToOutput("hahaa")
    printToOutput("")
    printToOutput("LISÄÄ LOGEJA TODEEEEEEELALLADLASDL\nasdhashdhas \nasdhjasjdasjd\sdjdsf")
    browser_lib.open_available_browser("https://www.etuovi.com/haku/myytavat-asunnot",headless=True)
    ovi=Etuovi()
    ovi.navigateToSearch()
    ovi.handlePage("https://www.etuovi.com/kohde/200asdasd86134")
    ovi.doSearch()
    
    allfFoundHrefs=ovi.getAllHrefs()
    resultDicts=[]
    for index,href in enumerate(allfFoundHrefs):
        if(index<120):
            continue
        printToOutput(index)
        result=ovi.handlePage(href)
        resultDicts.append(result)
        
    df = pd.DataFrame.from_records(resultDicts)
    df.to_excel("resultExcel2.xlsx")
    import os
    full_path = os.path.realpath(__file__)
    printToOutput("in __main__:"+"\n"+full_path + "\n")
    #
    #screen=sc.Screenshot()
    #path=sc.Screenshot().take_screenshot()