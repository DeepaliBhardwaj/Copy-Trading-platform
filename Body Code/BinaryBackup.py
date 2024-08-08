import threading
from json import load, dump
from os.path import exists
from subprocess import getstatusoutput
import pymongo

ParamsObject = {
    "IC_Status": False,
    "LocalMongoDB": False,
    "JSON": False
}

theCollections = ["eachStockData", "todaySumData", "averageData"]


def LocalMongoFunction():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TradeCollection']

    return db


def ServerMongo():
    clientI = pymongo.MongoClient(
        "mongodb+srv://rahul_vvishwakarma:sm79ViMRwG5QBJXc@cluster1.zrhednl.mongodb.net/?retryWrites=true&w=majority")
    db = clientI['TradeCollection']

    return db


def Notification(title, message, app_name, toast, timeout):
    from plyer import notification
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        toast=True,
        # displaying time
        timeout=5
    )


def JSONChecks():
    PendingCloudDataJSON = {
        "eachStockData": [],
        "todaySumData": [],
        "averageData": []
    }

    db = ServerMongo()

    for item in theCollections:
        collection = db[item]
        collectionData = []
        if exists(f"{item}.json"):
            with open(f"{item}.json", "r+") as data:
                file_data = load(data)
                for i in range(len(file_data[item])):
                    if file_data[item][i]["IC_Status"] == "Inactive":
                        PendingCloudDataJSON[item].append(i)
                        file_data[item][i]["IC_Status"] = "Active"
                        data.seek(0)
                        data.truncate()
                        dump(file_data, data, indent=4)
                        collectionData.append(file_data[item][i])

        collection.insert_many(collectionData) if len(collectionData) != 0 else 0


def MongoChecks():
    MongoStatus = getstatusoutput('mongod --version')[0]
    if MongoStatus:
        pass
    else:
        CollectionExistence = {
            "eachStockData": False,
            "todaySumData": False,
            "averageData": False
        }
        dbi = ServerMongo()
        db = LocalMongoFunction()
        iCollections = dbi.list_collection_names()
        lCollections = db.list_collection_names()

        for i in theCollections:
            if i in iCollections and i in lCollections:
                CollectionExistence[i] = True

        data = []

        for key in CollectionExistence.keys():
            if CollectionExistence[key]:

                collection = db[key].find({"IC_Status": "Inactive"}, {"_id": 0})
                for i in collection:
                    # data.append(i)

                    data.append(i)

                if len(data) > 0:
                    dbi[key].insert_many(data)

                    print(f"Inserted {len(data)} Documents of {key} Collection")
                    newValues = {"$set": {"IC_Status": "Active"}}

                    db[key].update_many({"IC_Status": "Inactive"}, newValues)



            else:
                '''Here the Code which will automatically create the new collection, Including It's Data from the Server'''
                # StorageCreationTool(False, False)  # PendingWork
                pass


def Trigger():
    JSONThread = threading.Thread(target=JSONChecks)
    MongoThread = threading.Thread(target=MongoChecks)
    JSONThread.start()
    MongoThread.start()
    JSONThread.join()
    MongoThread.join()


def ParamCheck():
    InternetStatus = int((getstatusoutput('ping -n 2 www.google.com >nul && echo 0 || echo 1'))[1])
    if InternetStatus == 0:
        ParamsObject["IC_Status"] = True
    else:
        ParamsObject["IC_Status"] = False

    if ParamsObject["IC_Status"]:
        Service1 = threading.Thread(target=Trigger)
        Service2 = threading.Thread(target=Notification, args=("Triggers - Activated", "Searching for Backups for Documents Now!", "StockAverage App", True, 1))
        Service1.start()
        Service2.start()


        Service1.join()
        Service2.join()

    else:
        if InternetStatus == 0:
            ParamsObject["IC_Status"] = True


ParamCheck()
