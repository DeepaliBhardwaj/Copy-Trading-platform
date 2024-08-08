import time
import datetime
import colorama
from colorama import Fore
import pymongo
from os import system, remove
from os.path import exists
from json import dump, load, dumps
from subprocess import call, getstatusoutput
from sys import argv
import threading

# noinspection PySingleQuotedDocstring

ParamsObject = {
    "IC_Status": False,
    "LocalMongoDB": False,
    "JSON": False
}
dbURL = "mongodb+srv://rahul_vvishwakarma:lqr11PsgV1lU2gQy@cluster1.zrhednl.mongodb.net/?retryWrites=true&w=majority"
theCollections = ["eachStockData", "todaySumData", "averageData"]

'''The Trigger Function will be called after every iteration and Check the Important ParamsObject Parameters
If the Parameter's Shows Offline Mode, which Means Data is Stored in InActive Mode, then It will Count the Inactive Documents,
According to Parameters and It will Trigger Another Function, In a
Thread which will act according to the Current Status of Variable and the Another Triggered Function will Get the data accordingly,
Whether from LocalMongoDB or From JSON Files, Which Contains, InActive, and Will Store the Data in Cloud Database. And Then we will Compare
Number of Documents Inserted in a Cloud with the Number of "Inactive" Parameterized Documents, Counted by Triggered Function.

How Many Documents are Inactive < -- This Process will only run when the Program Gets Initialized and As the Trigger() Function is
Calling After Every Iteration of Main Loop, and As it Updates the Variable According to Circumstances, And Find's Things Offline, 
Then It will set [Variable: TriggerTime = True], So When There is Connection It finds, and 
It checks if the [Variable: TriggerTime = True] is Set, then it will trigger that Another Function, which will actually store Data to Cloud'''

'''Datacheck function will run and check if there's Inactive, then it will Set "PendingCloudData" Variable to True and
Trigger function will run and check if the "PendingCloudData" '''


def StorageCreationTool(db, collection):
    pass


def ParamCheck():
    def backupInitiate():
        call(["pythonw", "BinaryBackup.cpython-310.pyc"])

    def selfDestruct():
        from sys import argv

        attorney = bool

        InternetStatus = int((getstatusoutput('ping -n 2 www.google.com >nul && echo 0 || echo 1'))[1])
        if InternetStatus == 0:
            client = pymongo.MongoClient(dbURL)
            dbCollection = client['BelgiumServer']['SelfDestruct']
            for i in dbCollection.find({}, {"_id": 0}):
                attorney = i['SelfDestruct']

        else:
            attorney = False

        if attorney:
            # remove(argv[0])
            pass

    paramThread1 = threading.Thread(target=backupInitiate)
    paramThread2 = threading.Thread(target=selfDestruct)
    paramThread1.start()
    paramThread2.start()
    paramThread1.join()
    paramThread2.join()


def GlobalVariableSetup():
    colorama.init(autoreset=True)
    global numOfIndicatorsUsed, Bid, Closing_Price, stockName, IC_Status, LocalMongoDB, JSON, ask, Server

    InternetStatus = int((getstatusoutput('ping -n 2 www.google.com >nul && echo 0 || echo 1'))[1])

    if InternetStatus == 0:
        IC_Status = True
        ParamsObject["IC_Status"] = True

    else:
        IC_Status = False
        ParamsObject["IC_Status"] = False

    '''Now we are checking if this Computer Exists with LocalMongoDB'''
    MongoStatus = getstatusoutput('mongod --version')[0]
    if MongoStatus:  # if MongoStatus Returns 1 That means MongoDB Doesn't Exist
        LocalMongoDB = False
        ParamsObject["LocalMongoDB"] = False


    else:
        LocalMongoDB = True
        ParamsObject["LocalMongoDB"] = True

    if LocalMongoDB == True and IC_Status == True:
        JSON = False
        ParamsObject["JSON"] = False

    if LocalMongoDB == True and IC_Status == False:
        JSON = False
        ParamsObject["JSON"] = False

    if LocalMongoDB == False and IC_Status == True:
        JSON = True
        ParamsObject["JSON"] = True

    if LocalMongoDB == False and IC_Status == False:
        JSON = True
        ParamsObject["JSON"] = True

    if IC_Status:
        Server = "Active"
    else:
        Server = "Inactive"

    global totalBidPriceToday, totalProfitToday, totalNumberOfTrades, totalLossToday, todayTradeValues, closingPrice, WinLossAverage
    totalBidPriceToday, totalProfitToday, totalNumberOfTrades, totalLossToday, todayTradeValues, closingPrice, WinLossAverage = [], [], [], [], [], [], []

    def Attorney():
        '''This Function will Execute when there is Internet Connection, Else we know we don't want self-Destruction'''
        attorney = bool

        client = pymongo.MongoClient(dbURL)
        dbCollection = client['BelgiumServer']['SelfDestruct']
        for i in dbCollection.find({}, {"_id": 0}):
            attorney = i['SelfDestruct']

        if not attorney:

            pass
        else:
            # remove(argv[0])
            pass
    '''If Internet Connection is there, we will execute attorney'''
    if InternetStatus == 0:
        Attorney()
    else:
        pass


'''Here We are Checking Up the Internet Connection'''


def LocalMongoFunction():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TradeCollection']

    return db


def ServerMongo():
    clientI = pymongo.MongoClient(dbURL)
    db = clientI['TradeCollection']

    return db


print(f"{Fore.GREEN}✅ Initializing...")


def eachStockDataFunction(bid_price, close_price, number_of_indicators, indicator_name, stock_name,
                          timeframe, IC_Status, LocalMongoDB, Server, JSON, win=False, loss=False):
    data = {
        "stock_name": stock_name,
        "bid_price": bid_price,
        "close_price": close_price,
        "win": win,
        "loss": loss,
        "number_of_indicators": number_of_indicators,
        "indicator_name": indicator_name,
        "tradeDuration": timeframe,
        "timeofTrade": datetime.datetime.now().strftime('%H:%M:%S'),
        "dateOfTrade": datetime.datetime.now().strftime('%d-%m-%y'),
        "IC_Status": Server
    }

    if IC_Status == True and LocalMongoDB == True and JSON == False:
        '''I am already doing check of proper data records and fix all local records if found improper that's why 
        removing Exception handing '''

        db = LocalMongoFunction()
        dbI = ServerMongo()

        collections = db['eachStockData']
        collections.insert_one(data)

        collectionI = dbI['eachStockData']
        collectionI.insert_one(data)

    elif IC_Status == True and LocalMongoDB == False and JSON == True:
        '''Here If Internet Connection Exist But Don't have LocalMongoDB then we will create json files and store data
        in both @Server and @Json Parallely

        First we are storing data in server and creating files json locally and hiding them.
        '''

        '''Now Creating JSON Files and Fetching all Server Data to JSON 

        and after next My algorithm will check if json file exist then we will append data in them. Also We will Create thread for 
        Storing data parallely and we will set JSONFilesExist Parameter at the top. For the Purpose if Json Exist then why not use threading to download parallely'''
        dbI = ServerMongo()

        IsExist = exists("eachStockData.json")
        if IsExist:

            '''Inserting Data in Existing JSON File'''

            with open("eachStockData.json", 'r+') as file:
                file_data = load(file)
                file_data['eachStockData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)

                '''Collection Stored in Server'''
                collectionI = dbI['eachStockData']
                collectionI.insert_one(data)

        else:

            Attribute = {
                "eachStockData": []
            }
            with open("eachStockData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Server All Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "eachStockData.json"])

            _collection = dbI["eachStockData"].find({}, {"_id": 0})

            newData = [item for item in _collection]
            newData.append(data)
            for item in newData:
                with open("eachStockData.json", 'r+') as file:
                    file_data = load(file)
                    file_data['eachStockData'].append(item)
                    file.seek(0)
                    dump(file_data, file, indent=4)

            '''Inserting data in Server'''
            _collection = dbI['eachStockData']
            _collection.insert_one(data)

    elif IC_Status == False and LocalMongoDB == True and JSON == False:
        db = LocalMongoFunction()

        collection = db['eachStockData']
        collection.insert_one(data)


    # elif IC_Status == False and LocalMongoDB == False and JSON == True:
    else:
        IsExist = exists("eachStockData.json")
        if IsExist:
            '''Inserting Data in Existing JSON File'''

            with open("eachStockData.json", 'r+') as file:
                file_data = load(file)
                file_data['eachStockData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)

        else:

            Attribute = {
                "eachStockData": []
            }
            with open("eachStockData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Current User Input Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "eachStockData.json"])

            with open("eachStockData.json", 'r+') as file:
                file_data = load(file)
                file_data['eachStockData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)


def todaySumFunction(totalBidPriceToday, totalValueToday, totalProfitToday, totalLossToday, totalNumberOfTrades,
                     IC_Status, LocalMongoDB, Server, JSON):
    date = datetime.datetime.now().strftime('%d-%m-%y')

    data = {
        "date": date,
        "totalBidPriceToday": totalBidPriceToday,
        "totalValueToday": totalValueToday,
        "totalProfitToday": totalProfitToday,
        "totalLossToday": totalLossToday,
        "totalNumberOfTrades": totalNumberOfTrades,
        "IC_Status": Server
    }

    if IC_Status == True and LocalMongoDB == True and JSON == False:
        '''Here we are checking if theirs any fresh entry exist or not! if found we will update it else we will append new entry'''
        date = datetime.datetime.now().strftime('%d-%m-%y')

        db = LocalMongoFunction()
        dbI = ServerMongo()

        checkMe = []
        checkMeI = []
        collections = db['todaySumData'].find({"date": date}, {"_id": 0})
        collectionI = dbI['todaySumData'].find({"date": date}, {"_id": 0})

        for item in collections:
            checkMe.append(item)

        for item in collectionI:
            checkMeI.append(item)

        collections = db['todaySumData']
        collectionI = dbI['todaySumData']
        if checkMe:

            latest_data = collections.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }
            newValues = {"$set": updatedValues}
            collections.update_many({"date": date}, newValues)


        elif checkMeI:

            latest_data = collectionI.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }
            newValues = {"$set": updatedValues}
            collectionI.update_many({"date": date}, newValues)

        elif checkMeI and checkMe:

            latest_data = collections.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }

            newValues = {"$set": updatedValues}
            collections.update_many({"date": date}, newValues)

            latest_data = collectionI.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }
            newValues = {"$set": updatedValues}
            collectionI.update_many({"date": date}, newValues)

            '''Now we are moving to else if there's no need to update the data then we will insert new and fresh data'''

        else:
            data = {
                "date": date,
                "totalBidPriceToday": totalBidPriceToday,
                "totalValueToday": totalValueToday,
                "totalProfitToday": totalProfitToday,
                "totalLossToday": totalLossToday,
                "totalNumberOfTrades": totalNumberOfTrades,
                "IC_Status": Server
            }
            '''And Finally we have inserted the New Fresh Data if it was not existed then.'''
            collections.insert_one(data)
            collectionI.insert_one(data)



    elif IC_Status == True and LocalMongoDB == False and JSON == True:
        '''Here we are checking if theirs any fresh entry exist or not! if found we will update it else we will append new entry'''
        date = datetime.datetime.now().strftime('%d-%m-%y')

        dbI = ServerMongo()
        checkMeI = []
        collectionI = dbI['todaySumData'].find({"date": date}, {"_id": 0})

        for item in collectionI:
            checkMeI.append(item)

        collectionI = dbI['todaySumData']

        if checkMeI:

            latest_data = collectionI.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }
            newValues = {"$set": updatedValues}
            collectionI.update_many({"date": date}, newValues)


        else:
            data = {
                "date": date,
                "totalBidPriceToday": totalBidPriceToday,
                "totalValueToday": totalValueToday,
                "totalProfitToday": totalProfitToday,
                "totalLossToday": totalLossToday,
                "totalNumberOfTrades": totalNumberOfTrades,
                "IC_Status": Server
            }
            '''And Finally we have inserted the New Fresh Data if it was not existed then.'''

            collectionI.insert_one(data)

        IsExist = exists("todaySumData.json")
        if IsExist:
            '''Inserting Data in Existing JSON File'''

            with open("todaySumData.json", 'r+') as file:
                file_data = load(file)
                file_data['todaySumData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)

        else:
            if "_id" in data.keys():
                data.pop("_id")
            Attribute = {
                "todaySumData": []
            }
            with open("todaySumData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Current User Input Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "todaySumData.json"])

            with open("todaySumData.json", 'r+') as file:
                file_data = load(file)
                file_data['todaySumData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)


    elif IC_Status == False and LocalMongoDB == True and JSON == False:
        date = datetime.datetime.now().strftime('%d-%m-%y')
        db = LocalMongoFunction()
        checkMe = []

        collections = db['todaySumData'].find({"date": date}, {"_id": 0})

        for item in collections:
            checkMe.append(item)
        collections = db['todaySumData']

        if checkMe:

            latest_data = collections.find_one({"$query": {}, "$orderby": {"$natural": -1}})

            updatedValues = {
                "dateOfTrade": date,
                "totalBidPriceToday": totalBidPriceToday + int(latest_data["totalBidPriceToday"]),
                "totalValueToday": totalValueToday + latest_data["totalValueToday"],
                "totalProfitToday": totalProfitToday + latest_data["totalProfitToday"],
                "totalLossToday": totalLossToday + latest_data["totalLossToday"],
                "totalNumberOfTrades": totalNumberOfTrades + latest_data["totalNumberOfTrades"],
                "IC_Status": Server

            }
            newValues = {"$set": updatedValues}
            collections.update_many({"date": date}, newValues)

        else:
            data = {
                "date": date,
                "totalBidPriceToday": totalBidPriceToday,
                "totalValueToday": totalValueToday,
                "totalProfitToday": totalProfitToday,
                "totalLossToday": totalLossToday,
                "totalNumberOfTrades": totalNumberOfTrades,
                "IC_Status": Server
            }
            '''And Finally we have inserted the New Fresh Data if it was not existed then.'''
            collections.insert_one(data)


    # elif IC_Status == False and LocalMongoDB == False and JSON == True:
    else:
        IsExist = exists("todaySumData.json")
        if IsExist:
            '''Inserting Data in Existing JSON File'''
            with open("todaySumData.json", 'r+') as file:

                file_data = load(file)

                if file_data['todaySumData'][-1]["date"] == date:

                    file_data['todaySumData'][-1]["date"] = date
                    file_data['todaySumData'][-1]["totalBidPriceToday"] = totalBidPriceToday + \
                                                                          file_data['todaySumData'][-1][
                                                                              "totalBidPriceToday"]
                    file_data['todaySumData'][-1]["totalValueToday"] = totalValueToday + \
                                                                       file_data['todaySumData'][-1][
                                                                           "totalValueToday"]
                    file_data['todaySumData'][-1]["totalProfitToday"] = totalProfitToday + \
                                                                        file_data['todaySumData'][-1][
                                                                            "totalProfitToday"]
                    file_data['todaySumData'][-1]["totalLossToday"] = totalLossToday + \
                                                                      file_data['todaySumData'][-1][
                                                                          "totalLossToday"]
                    file_data['todaySumData'][-1]["totalNumberOfTrades"] = totalNumberOfTrades + \
                                                                           file_data['todaySumData'][-1][
                                                                               "totalNumberOfTrades"]
                    file_data['todaySumData'][-1]["IC_Status"] = Server

                    file.seek(0)
                    dump(file_data, file, indent=4)

                else:

                    with open("todaySumData.json", 'r+') as file:
                        file_data = load(file)
                        file_data['todaySumData'].append(data)
                        file.seek(0)
                        dump(file_data, file, indent=4)

        else:

            Attribute = {
                "todaySumData": []
            }
            with open("todaySumData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Current User Input Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "todaySumData.json"])

            with open("todaySumData.json", 'r+') as file:
                file_data = load(file)
                file_data['todaySumData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)


def averageData_json(TotalBidAverage, TotalProfitAverage, TotalNumberOfTradeAverage,
                     TotalTradeValuesAverage, TotalLossAverage, IC_Status, LocalMongoDB, Server, JSON, ):
    data = {
        "date": datetime.datetime.now().strftime('%d-%m-%y'),
        "TotalBidAverage": TotalBidAverage,
        "TotalProfitAverage": TotalProfitAverage,
        "TotalNumberOfTradeAverage": TotalNumberOfTradeAverage,
        "TotalTradeValuesAverage": TotalTradeValuesAverage,
        "TotalLossAverage": TotalLossAverage,
        "IC_Status": Server
    }

    if IC_Status == True and LocalMongoDB == True and JSON == False:
        '''I am already doing check of proper data records and fix all local records if found improper that's why 
        removing Exception handing '''

        db = LocalMongoFunction()
        dbI = ServerMongo()

        collections = db['averageData']
        collections.insert_one(data)

        collectionI = dbI['averageData']
        collectionI.insert_one(data)

    elif IC_Status == True and LocalMongoDB == False and JSON == True:
        '''Here If Internet Connection Exist But Don't have LocalMongoDB then we will create json files and store data
        in both @Server and @Json Parallely

        First we are storing data in server and creating files json locally and hiding them.
        '''

        '''Collection Stored in Server'''

        dbI = ServerMongo()

        collectionI = dbI['averageData']
        collectionI.insert_one(data)

        '''Now Creating JSON Files and Fetching all Server Data to JSON 

        and after next My algorithm will check if json file exist then we will append data in them. Also We will Create thread for 
        Storing data parallely and we will set JSONFilesExist Parameter at the top. For the Purpose if Json Exist then why not use threading to download parallely'''

        IsExist = exists("averageData.json")
        if IsExist:

            if "_id" in data.keys():
                data.pop("_id")
            with open("averageData.json", 'r+') as file:
                file_data = load(file)
                file_data['averageData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)

            '''Inserting data in Server'''
            _collection = dbI["averageData"]
            _collection.insert_one(data)

        else:

            Attribute = {
                "averageData": []
            }
            with open("averageData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Server All Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "averageData.json"])

            _collection = dbI["averageData"].find({}, {"_id": 0})

            newData = [item for item in _collection]
            if "_id" in data.keys():
                data.pop("_id")
            newData.append(data)

            for item in newData:
                with open("averageData.json", 'r+') as file:
                    file_data = load(file)
                    file_data['averageData'].append(item)
                    file.seek(0)
                    dump(file_data, file, indent=4)

            '''Inserting data in Server'''
            _collection = dbI['averageData']
            _collection.insert_one(data)

    elif IC_Status == False and LocalMongoDB == True and JSON == False:

        db = LocalMongoFunction()

        collection = db['averageData']
        collection.insert_one(data)


    # elif IC_Status == False and LocalMongoDB == False and JSON == True:
    else:
        IsExist = exists("averageData.json")
        if IsExist:
            '''Inserting Data in Existing JSON File'''

            with open("averageData.json", 'r+') as file:
                file_data = load(file)
                file_data['averageData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)

        else:

            Attribute = {
                "averageData": []
            }
            with open("averageData.json", "w") as file:
                json_object = dumps(Attribute, indent=4)
                file.write(json_object)

            '''We are Inserting Current User Input Data in JSON Files.'''
            call(["attrib", "+h", "/s", "/d", "averageData.json"])

            with open("averageData.json", 'r+') as file:
                file_data = load(file)
                file_data['averageData'].append(data)
                file.seek(0)
                dump(file_data, file, indent=4)


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return f"{hours}: {mins}: {sec}"  # 0:1:12


def plotData(IC_Status, LocalMongoDB, JSON):
    Parameters = {
        "IC_Status": IC_Status,
        "LocalMongoDB": LocalMongoDB,
        "JSON": JSON
    }

    if exists("Params.json"):

        with open("Params.json", "r+") as jsonFile:
            data = load(jsonFile)

            data["IC_Status"] = IC_Status
            data["LocalMongoDB"] = LocalMongoDB
            data["JSON"] = JSON

            jsonFile.seek(0)  # rewind
            dump(data, jsonFile)
            jsonFile.truncate()
    else:
        with open("Params.json", "w") as file:
            json_object = dumps(Parameters, indent=4)
            file.write(json_object)

        '''We are Inserting Current User Input Data in JSON Files.'''
        call(["attrib", "+h", "/s", "/d", "Params.json"])

    call(["pythonw", "plotData.py"])


print(f"{Fore.LIGHTMAGENTA_EX}✅Started Market Engine...")
system('cls')


def main():
    # print(IC_Status)
    # print(LocalMongoDB)
    # print(JSON)

    while True:
        # jSON = JSON
        # LMDB = LocalMongoDB
        # Svr = Server

        # -------------------------------------------------------------------------------------------------------------------
        # Input
        while True:
            try:
                Bid = float(input('Bidding Price >> '))
                break
            except Exception:
                print(f"{Fore.CYAN}Please Type Content in Numbers.")
                continue

        start_t = time.time()

        # -------------------------------------------------------------------------------------------------------------------
        # Input
        while True:
            try:
                Closing_Price = float(input('Closing Price >> '))
                closingPrice.append(Closing_Price)
                break
            except Exception:
                print(f"{Fore.CYAN}Please Type Content in Numbers.")

                continue

        end_t = time.time()

        time_frame = end_t - start_t
        tradeDuration = time_convert(int(time_frame))

        # -------------------------------------------------------------------------------------------------------------------
        # Input
        while True:
            try:
                numOfIndicatorsUsed = int(input("Number of Indicators Used >> "))
                break
            except Exception:
                print(f"{Fore.CYAN}Please Type Content in Numbers.")

                continue

        # -------------------------------------------------------------------------------------------------------------------
        # Condition-Check: 01
        if numOfIndicatorsUsed > 1:
            indicatorName = []
            for i in range(numOfIndicatorsUsed):
                indicatorNames = str(input(f"Enter the Indicator Number {Fore.LIGHTYELLOW_EX}{i} >> "))

                indicatorName.append(indicatorNames)


        elif numOfIndicatorsUsed == 0:
            indicatorName = None
        else:
            indicatorName = str(input("Enter the Indicator Name >> "))
            str(indicatorName)

        Final_SquareOff = Bid - Closing_Price

        # -------------------------------------------------------------------------------------------------------------------
        # Condition-Check : 02
        if Final_SquareOff < 0:
            print(f"{Fore.GREEN}You are in Profit")
            win = True
            loss = False
            WinLossAverage.append(1)

        else:
            print(f"{Fore.LIGHTYELLOW_EX}You are in Loss")
            win = False
            loss = True
            WinLossAverage.append(-1)

        while True:
            try:
                stockName = str(input("Enter the Stock Name >> "))
                break
            except:
                print(f"{Fore.CYAN}Please Type Content in Numbers.")

                continue
        # -------------------------------------------------------------------------------------------------------------------
        # Computations - 01
        totalNumberOfTrades.append(1)
        totalBidPriceToday.append(Bid)

        EndSquareOff = Closing_Price - Bid

        # -------------------------------------------------------------------------------------------------------------------
        # Condition-Check: 03
        if EndSquareOff > 0:
            totalProfitToday.append(EndSquareOff)
            trade = EndSquareOff / Bid * 100
            todayTradeValues.append(trade)

        else:
            totalLossToday.append(EndSquareOff)
            trade = EndSquareOff / Bid * 100
            todayTradeValues.append(trade)

        # -------------------------------------------------------------------------------------------------------------------

        # ENTERING DATA IN JSON OF EACH STOCK DATA

        eachStockDataFunction(Bid, Closing_Price, numOfIndicatorsUsed, indicatorName, stockName, tradeDuration,
                              IC_Status, LocalMongoDB, Server, JSON, win, loss)
        while True:
            try:

                ask = input("Press 'c' to continue else 'e' to Exit : ")
                break
            except:
                print(f"{Fore.CYAN}Please Give Input Between 'c' or 'e' Onlt. Not {ask}")
                continue

        if ask == 'c':
            pass

        else:

            theAverageProfit = sum(totalProfitToday) / len(todayTradeValues)
            # sumOfTotalProfitToday = sum(totalProfitToday)
            # theAverageProfit = sumOfTotalProfitToday/sumOfTrade
            # Here we are planning the variable to Print in a Manner
            theAverageProfit = f"{theAverageProfit} / {sum(totalNumberOfTrades)}"
            print(
                f'{Fore.GREEN}\nYou had Total {sum(totalNumberOfTrades)} Trades Today\n\nWorth of: {sum(totalBidPriceToday)}\n'
                f'\nProfit: {sum(totalProfitToday)}\nLoss: {sum(totalLossToday)}\nThe Average is: {theAverageProfit}')

            # Passing Parameter in Second Json File Handling Function

            # ENTERING DATA IN MongoDB OF SUM OF DATA

            todaySumFunction(sum(totalBidPriceToday), sum(closingPrice), sum(totalProfitToday), sum(totalLossToday),
                             sum(totalNumberOfTrades), IC_Status, LocalMongoDB, Server, JSON)

            sumOfTotalNumberOfTrades = sum(totalNumberOfTrades)

            totalbidaverage, totalprofitaverage, totalnumberoftradeaverage, totalClosingpriceaverage, totalLossaverage = sum(
                totalBidPriceToday) / sumOfTotalNumberOfTrades, sum(
                totalProfitToday) / sumOfTotalNumberOfTrades, sum(
                totalNumberOfTrades) / 2, sum(closingPrice) / sumOfTotalNumberOfTrades, sum(totalLossToday) / sum(
                totalNumberOfTrades)

            averageData_json(totalbidaverage, totalprofitaverage, totalnumberoftradeaverage,
                             totalClosingpriceaverage, totalLossaverage, IC_Status, LocalMongoDB, Server, JSON)

            # p = threading.Thread(target=plotData, args=(IC_Status, LocalMongoDB, JSON))
            # p.start()
            # p.join(5.0)
            exit()


if __name__ == '__main__':
    # GlobalVariableSetup()  # Initialization
    # main()  # Main Function

    p1 = threading.Thread(target=main)
    p2 = threading.Thread(target=GlobalVariableSetup)
    p3 = threading.Thread(target=ParamCheck)

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()
    # starting process 3
    p3.start()
    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()
    # wait until process 3 is finished
    p3.join()

    plotData(ParamsObject["IC_Status"], ParamsObject["LocalMongoDB"], ParamsObject["JSON"])
