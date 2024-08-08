import pymongo

theCollections = ['eachStockData', 'todaySumData', 'averageData']

clientI = pymongo.MongoClient("mongodb+srv://rahul_vvishwakarma:rANDO8a5Hekkt38W@cluster1.zrhednl.mongodb.net/?retryWrites=true&w=majority")
db = clientI['TradeCollection'][theCollections[0]].find({})

for i in db:
    print(i)
