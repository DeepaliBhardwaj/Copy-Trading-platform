import pymongo
import numpy as np
import matplotlib.pyplot as plt
import datetime
from os.path import exists
from json import load


def LocalMongoFunction():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['TradeCollection']

    return db


def ServerMongo():
    clientI = pymongo.MongoClient(
        "mongodb+srv://rahul_vvishwakarma:lqr11PsgV1lU2gQy@cluster1.zrhednl.mongodb.net/?retryWrites=true&w=majority")
    db = clientI['TradeCollection']

    return db


def plotData(IC_Status, LocalMongoDB, JSON):
    row = 2
    column = 3
    bid_price, close_price, number_of_indicators, tradeDuration, win, fresh_buy, fresh_sell, fresh_win = [], [], [], [], [], [], [], []

    date = datetime.datetime.now().strftime('%d-%m-%y')
    if LocalMongoDB == False and IC_Status == False and JSON == True:
        if exists('eachStockData.json'):
            with open('eachStockData.json', 'r') as file:
                file_data = load(file)
                for item in file_data['eachStockData']:
                    bid_price.append(item['bid_price'])
                    close_price.append(item['close_price'])

                    number_of_indicators.append(item['number_of_indicators'])

                    tradeDuration.append(item['tradeDuration'])

                    win.append(item['win'])
                    if item["dateOfTrade"] == date:
                        fresh_buy.append(item['bid_price'])
                        fresh_sell.append(item['close_price'])
                        fresh_win.append(item['win'])

            coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators,
                          fresh_buy, fresh_sell, fresh_win)

        else:
            coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators, fresh_buy,
                          fresh_sell, fresh_win)
    else:

        if LocalMongoDB == True and IC_Status == True and JSON == False:
            db = LocalMongoFunction()
            collection = db['eachStockData']
            data = collection.find("", {"_id": 0})
            for item in data:
                bid_price.append(item['bid_price'])
                close_price.append(item['close_price'])

                number_of_indicators.append(item['number_of_indicators'])

                tradeDuration.append(item['tradeDuration'])

                win.append(item['win'])

            FreshTrade = collection.find({"dateOfTrade": date}, {'_id': 0})

            for item in FreshTrade:
                fresh_buy.append(item['bid_price'])
                fresh_sell.append(item['close_price'])
                fresh_win.append(item['win'])

            coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators, fresh_buy,
                          fresh_sell, fresh_win)

        if LocalMongoDB == True and IC_Status == False and JSON == False:
            db = LocalMongoFunction()
            collection = db['eachStockData']
            data = collection.find("", {"_id": 0})
            for item in data:
                bid_price.append(item['bid_price'])
                close_price.append(item['close_price'])

                number_of_indicators.append(item['number_of_indicators'])

                tradeDuration.append(item['tradeDuration'])

                win.append(item['win'])

            FreshTrade = collection.find({"dateOfTrade": date}, {'_id': 0})

            for item in FreshTrade:
                fresh_buy.append(item['bid_price'])
                fresh_sell.append(item['close_price'])
                fresh_win.append(item['win'])

            coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators, fresh_buy,
                          fresh_sell, fresh_win)

        if LocalMongoDB == False and IC_Status == True and JSON == True:
            dbI = ServerMongo()
            collection = dbI['eachStockData']

            data = collection.find("", {"_id": 0})

            for item in data:
                bid_price.append(item['bid_price'])
                close_price.append(item['close_price'])

                number_of_indicators.append(item['number_of_indicators'])

                tradeDuration.append(item['tradeDuration'])

                win.append(item['win'])

            FreshTrade = collection.find({"dateOfTrade": date}, {'_id': 0})

            for item in FreshTrade:
                fresh_buy.append(item['bid_price'])
                fresh_sell.append(item['close_price'])
                fresh_win.append(item['win'])

            coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators, fresh_buy,
                          fresh_sell, fresh_win)


def coregraphplot(row, column, bid_price, close_price, win, tradeDuration, number_of_indicators, fresh_buy,
                  fresh_sell, fresh_win):
    xAxis = np.array(range(1, len(close_price) + 1))

    '''Graph - 01'''

    plt.subplot(row, column, 1)
    plt.plot(xAxis, close_price, 'g', label="Closing Price")
    plt.plot(xAxis, bid_price, 'r', label="Bid Price")
    plt.xlabel('Range')
    plt.ylabel('Prices')
    plt.title("Trade Perception of Today Each")

    plt.legend()

    '''Graph - 02'''

    xAxis = np.array(range(1, len(number_of_indicators) + 1))
    plt.subplot(row, column, 2)
    plt.plot(xAxis, number_of_indicators, 'g', label="Number of Indicators")
    plt.xlabel('Range')
    plt.ylabel('Number of Indicators Used By Time')
    plt.title("Number of Indicators Used")

    plt.legend()

    '''Graph - 03'''
    Hour = False
    Minute = False
    Second = False
    for string in tradeDuration:
        timeList = string.split(": ")
        times = [eval(i) for i in timeList]

        if times[0] != 0:
            # print('its hour')
            Hour = True
        elif times[1] != 0:
            # print('its minute')
            Minute = True
        else:
            # print('its second')
            Second = True

    # print(Hour, Minute, Second)
    Decision = []
    if Hour:
        # print("its hour time")
        Decision.append("Hours")
    if Minute:
        # print("its Minute time")
        Decision.append("Minutes")
    if Second:
        # print("its Second time")
        Decision.append("Seconds")

    timeUnit = Decision[0]
    # print((''.join(string.split(": ")))[0])
    xAxis = np.array(range(1, len(tradeDuration) + 1))

    tradeDurationUpdate = []
    for items in tradeDuration:
        tradeDurationUpdate.append(int(''.join(items.split(": "))))

    plt.subplot(row, column, 3)
    plt.plot(xAxis, np.array(tradeDurationUpdate), 'g', label=f"TD in {timeUnit}")
    plt.xlabel('Range')
    plt.ylabel(f"TD in {timeUnit}")
    plt.title(f"TD in {timeUnit}")

    plt.legend()

    '''Graph - 04'''
    yPoints = []
    length = len(win)
    plt.subplot(row, column, 4)
    if length > 1:

        for i in range(len(win)):

            if i == 0:
                number = win[i] + win[i + 1]


            elif (length - 1) == i:
                break
            else:
                number = yPoints[-1] + win[i + 1]

            yPoints.append(number)

        label = 'Trades Successor'
        color = 'g'
        xAxis = np.array(range(1, len(win)))
        yAxis = yPoints

        plt.plot(np.array(xAxis), np.array(yAxis), color, label=label)
        plt.plot(np.array(xAxis), np.array(yAxis), color, label='1/-1 Binaries of All Time')
    else:
        xAxis = np.array(range(1, len(win)))
        yAxis = yPoints
        color = 'r'
        label = 'Trades Successor/ Insufficient Data.'
        plt.plot(np.array(xAxis), np.array(yAxis), color, label=label)
        plt.plot(np.array(xAxis), np.array(yAxis), color, label='Do More than a Trade for Graph')

    plt.xlabel('Range')
    plt.ylabel('Trades Profit/Loss Chart')
    plt.title("All Time Profit/Loss Using Binaries")
    plt.legend()

    '''Graph - 05'''
    plt.subplot(row, column, 5)
    xAxis = np.array(range(1, len(fresh_buy) + 1))
    if len(fresh_sell) == 0:
        color = 'r'
        label = 'Zero Trade Executed'

        plt.plot(np.array(xAxis), np.array(fresh_buy), color, label=label)

    else:
        buying = 'g'
        selling = 'r'
        buying_label = "Buying Price"
        selling_label = "Selling Price"

        plt.plot(np.array(xAxis), np.array(fresh_buy), buying, label=buying_label)
        plt.plot(np.array(xAxis), np.array(fresh_sell), selling, label=selling_label)
        plt.plot([0], [0], 'y', label=f"{sum(fresh_buy)} Total Investment")
        plt.plot([0], [0], 'm', label=f"{sum(fresh_sell)} Current Value")
        plt.plot([0], [0], 'k', label=f"{(sum(fresh_sell)) - (sum(fresh_buy))} Day P&L")

    plt.xlabel('Range')
    plt.ylabel("Today's Fresh Trades Buying-Selling Prices")
    plt.title("Today's Fresh Data")
    plt.legend()

    '''Graph - 06'''
    plt.subplot(row, column, 6)

    length = len(fresh_win)

    yPoints = []
    if length > 1:
        for i in range(len(fresh_win)):

            if i == 0:
                number = fresh_win[i] + fresh_win[i + 1]


            elif (length - 1) == i:
                break
            else:
                number = yPoints[-1] + fresh_win[i + 1]

            yPoints.append(number)
            color = 'm'
            label = 'Day P&L Trades Successor'

    else:
        color = 'r'
        label = 'Insufficient Data'

    xAxis = np.array(range(1, len(fresh_win)))
    yAxis = yPoints

    plt.plot(np.array(xAxis), np.array(yAxis), color, label=label)
    plt.xlabel('Range')
    plt.ylabel('Day Trade P&L Chart')
    plt.title("Day P&L Using Binaries")
    plt.legend()

    plt.subplots_adjust(top=0.952, bottom=0.078, left=0.058, right=0.99, hspace=0.275, wspace=0.192)

    plt.show()




with open("Params.json", "r") as file:
    file_data = load(file)
    IC_Status = file_data["IC_Status"]
    LocalMongoDB = file_data["LocalMongoDB"]
    JSON = file_data["JSON"]
    plotData(IC_Status, LocalMongoDB, JSON)