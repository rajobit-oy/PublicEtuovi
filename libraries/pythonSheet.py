"""
muuttujia"""
LIBRARY=""
ID="16wUrf8YvQ1KpIdwqXCHw7XqtBpUua7dHEYLO1_De6qA"
SHEET_RANGE="2022!A:U"

from robot.libraries.BuiltIn import BuiltIn
from RPA.Cloud.Google import Google
import traceback
class pythonSheet:
    def testInsertValues(self,id,range,values):
        vars=BuiltIn().log_variables()
        #RPA.Cloud.Google.insert_sheet_values()
        BuiltIn().run_keyword("RPA.Cloud.Google.Insert Sheet Values",id,range,values,"ROWS")

        print("")

    def createLibrary(self):
        vault_name="GoogleSheets"
        vault_secret_key="service_account"
        global LIBRARY
        if(not LIBRARY):
            LIBRARY = Google(vault_name=vault_name,vault_secret_key=vault_secret_key)
            LIBRARY.init_drive(use_robocorp_vault=True)
            LIBRARY.init_sheets(use_robocorp_vault=True)

    def errorr(self):
        raise Exception("testi exception")


    def addEsite(self,valuesDict):
        """
        Adds esite to our googledrive
        After adding esite, collects links to googledrive and adds them to values.
        adds values to our googlesheet.
        
        """
        print("creating library")
        self.createLibrary()
        fullPath=valuesDict["LocalFile"]
        name=valuesDict["Nimi"]
        print(f"creating directory named:{name}")
        createdID=createDirectory(name)
        url=f"https://drive.google.com/drive/u/1/folders/{createdID}"
        print(f"directory url={url} of created directory")
        testExists(name)
        for i in range(5):
            try:
                print(f"Uploading to drive trytime:{i}")
                print(f"fullPath={fullPath} name={name}")
                uploadResult=LIBRARY.upload_drive_file(fullPath,name,overwrite=False)
                break
            except Exception as e:
                print(str(e)+"\n"+traceback.format_exc())
                if(i==9):
                    raise
        print(uploadResult)
        print("")
        fileLink=f"https://drive.google.com/file/d/{uploadResult}/view?usp=sharing"
        #values+=[url,fileLink]
        valuesDict["KansioPolku"]=url
        valuesDict["Kuvat"]=fileLink
        values=list(valuesDict.values())
        LIBRARY.insert_sheet_values(ID,SHEET_RANGE,[values],"ROWS")
        return url

def testExists(folderId):
    allFiles=LIBRARY.list_shared_drive_files(f'name = "{folderId}"',source="EtuoviPython")#,#)
    print(allFiles)
    print("")

def createDirectory(folderName):
    """tekee directoryn
    Google drive toimii siten että jos on jo olemassa sitä ei tehdävaan palautetaan vaan
    """
    
    #if(not allFiles):
    new_directory=LIBRARY.create_drive_directory(folderName,parent_folder="EtuoviPython")
    #else:
    #    new_directory=allFiles[0]
    return new_directory["id"]   




if __name__ == "__main__":


    import os
    import json
    full_path = os.path.realpath(__file__)
    print("in __main__:"+full_path + "\n")
    service_account = r"C:\Users\matti\Downloads\service_account.json"
    LIBRARY = Google(service_account=service_account)
    LIBRARY.init_drive(service_account)
    LIBRARY.init_sheets(service_account)
    #Uudern directoryn teko:
    #new_directory=library.create_drive_directory("etuovi_pykansio_1234",parent_folder="EtuoviPython")#"1G0O7-71VmdvtP1vlW57Gl6y5_YC8mC3Z")
    #print(new_directory)
    folderId="Sointulantie 10 A7, Keskusta, Ruovesi"
    path=r"C:\Users\matti\Documents\RBCORP\Etuovi\output\526377\esite.pdf"
    
    pythonSheetc=pythonSheet()
    with open(r"output\526377\result.json", "r",encoding="UTF-8") as file:                  
        everything=file.read()
        dictV=json.loads(everything)
    pythonSheetc.addEsite(dictV)
    print("")
    
    #allFiles=library.list_shared_drive_files('name contains "etuovi"',source="EtuoviPython")
    #createDirectory(folderId)
    #createDirectory(folderId)
    #library.insert_sheet_values(id,sheet_range,[['Mark', 'The Monkey', 100000, 10000,"hahaa"]],"ROWS")