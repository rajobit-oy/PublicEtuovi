
from RPA.Robocorp.Process import Process
from RPA.Robocorp.Vault import Vault
##from RPA.Robocorp.WorkItems import WorkItems 
#WorkItems.st

#['IN_PROGRESS', 'FAILED', 'COMPLETED']
#['IN_PROGRESS', 'FAILED', 'COMPLETED', 'NEW', 'PENDING']
states=[]
import json
process=None
def list_process_work_items_own(
        process_id = None,
        include_data=False,
        item_state=None,
        cursor=None,
        collectedData=None
    ):
    """Own version of list_process_work_items
    That has the possibility to get over 100 items.
    This is recursive function.
    """

    params={"includeData": str(include_data).lower()}
    if(cursor):
        params["cursor"]=cursor
    if(item_state):
        params["state"]=item_state
    response = process.http.session_less_get(url=f"{process.process_api(process_id)}/work-items",headers=process.headers,
        params=params
    )
    print(response)
    response.raise_for_status()
    jsonVal=response.json()
    with open("tiedosto2.json", "w+",encoding="utf-8") as file:
        json.dump(jsonVal,file, sort_keys=True, indent=4, separators=(",", ": "))
    nextCurosr=jsonVal["nextCursor"]
    print(nextCurosr)
    if(not collectedData):
        collectedData=jsonVal["data"]
    else:
        collectedData+=jsonVal["data"]
    if(nextCurosr):

        return list_process_work_items_own(process_id=process_id,include_data=include_data,item_state=item_state,cursor=nextCurosr,collectedData=collectedData)
    else:
        with open("finalData.json", "w+",encoding="utf-8") as file:
            json.dump(collectedData,file, sort_keys=True, indent=4, separators=(",", ": "))
        return collectedData

def get_work_items():
    global states
    items=list_process_work_items_own(include_data=True)
    #completed_items = process.list_process_work_items(include_data=True,item_state="COMPLETED")
    #items=process.list_process_work_items(include_data=True)
    completed_filtered=[]
    for item in items:
        #print("work item: %s" % item["id"])
        print(item["state"])
        if(item["state"] not in states):
            states.append(item["state"])
        #print(f"payload:{item['payload']}")
        if item["state"] == "COMPLETED":
            completed_filtered.append(item)

CACHED_ITEMS=[]

def work_item_with_value_exists(value,key="id",use_cache=True):
    """Gets all work items and caches them if wanted.
    Checks if value exists in given key of workitem payload.

    """
    global CACHED_ITEMS
    if(use_cache):
        if(CACHED_ITEMS):
            items=CACHED_ITEMS
        else:
            items=[]
    else:
        items=[]
    if(not items):
        items = list_process_work_items_own(include_data=True)
        if(use_cache):
            CACHED_ITEMS=items
    if(items):
        for item in items:
            if(item["state"] != "FAILED"):
                payload=item['payload']
                if(payload and key in item['payload'].keys()):
                    if(item['payload'][key]==value):
                        return True
    return False

class robocorpapi():
    def setup(self):
        global process
        secrets = Vault().get_secret("ProcessAPI")
        process = Process(
            secrets["workspace_id"],
            secrets["process_id"],
            secrets["apikey"]
        ) 
    def item_with_key_exists(self,id,key="id",use_cache=True):
        """Gets all work items and caches them if wanted.
        Checks if value exists in given key of workitem payload.

        """
        global process
        if(not process):
            secrets = Vault().get_secret("ProcessAPI")
            process = Process(
                secrets["workspace_id"],
                secrets["process_id"],
                secrets["apikey"]
            ) 
        return work_item_with_value_exists(id,key=key,use_cache=use_cache)
    def testResults(self):
        global process
        secrets = Vault().get_secret("ProcessAPI")
        process = Process(
            secrets["workspace_id"],
            secrets["process_id"],
            secrets["apikey"]
        ) 
        #
        import time
        exists=work_item_with_value_exists("21250502")
        exists2=work_item_with_value_exists("21250502asd")
        print(f"value:{exists}")
        for i in range(10000):
            get_work_items()
            time.sleep(0.4)        

    def test(self):
        import os
        import json
        #with open("environ.json", "w+",encoding="utf-8") as file:
        #    json.dump(environ,file, sort_keys=True, indent=4, separators=(",", ": "))
        
        dictr={
            "RC_API_SECRET_HOST":os.environ["RC_API_SECRET_HOST"],
            "RC_API_SECRET_TOKEN":os.environ["RC_API_SECRET_TOKEN"],
            "RC_WORKSPACE_ID":os.environ["RC_WORKSPACE_ID"]
        }
        with open("dictr.json", "w+",encoding="utf-8") as file:
            json.dump(dictr,file, sort_keys=True, indent=4, separators=(",", ": "))
                    
        secrets = Vault().get_secret("robotsparebin")
        print(secrets)
        print(secrets["username"])
        print("")



if __name__ == "__main__":
    from robocorpapi_test import setEnv
    setEnv()
    #secrets = Vault().get_secret("robotsparebin")
    secrets = Vault().get_secret("ProcessAPI")
    process = Process(
        secrets["workspace_id"],
        secrets["process_id"],
        secrets["apikey"]
    ) 
    #
    import time
    for i in range(10000):
        get_work_items()
        time.sleep(0.4)