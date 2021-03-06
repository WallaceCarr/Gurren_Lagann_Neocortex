from ObservanceObject import ObservanceObject
from TimeManager import TimeManager


class ScenarioManager:
    def __init__(self):
        self.chronIdentifierStartList = ["10","35"]
        self.chronIdentifierBeginWatchList = ["11","5"]
        self.chronIdentifierEndWatchList = ["12","35"]

    def calculateFullRangeResults(self, fullRangeSet):
        observanceObject = ObservanceObject()
        observanceObject.setFullRangeSet(fullRangeSet)
        observanceObject.setBoughtBidPrice(fullRangeSet[(len(fullRangeSet) - 1)]["bid"])
        observanceObject.setHighDelimiter(.01)
        observanceObject.setLowDelimiter(.05)

        self.calculateWinOrLoseFullRange(observanceObject)
        return observanceObject

    def calculateMarkationResults(self, markationList):
        markationResults = []
        for markationSet in markationList:
            observanceObject = ObservanceObject()
            observanceObject.setMarkationSet(markationSet)
            observanceObject.setBoughtBidPrice(markationSet[0]["bid"])
            observanceObject.setHighDelimiter(.01)
            observanceObject.setLowDelimiter(.05)

            self.calculateWinOrLoseMarkation(observanceObject)
            markationResults.append(observanceObject)
        return markationResults

    def calculateFullRangeMarkationResults(self, stockRangeContainerTenMinuteSetComposite):
        markationResults = []
        for tenMinuteSet in stockRangeContainerTenMinuteSetComposite:
            observanceObject = ObservanceObject()
            observanceObject.setMarkationSet(tenMinuteSet)
            observanceObject.setBoughtBidPrice(tenMinuteSet[0]["bid"])
            observanceObject.setHighDelimiter(.01)
            observanceObject.setLowDelimiter(.05)

            self.calculateWinOrLoseFullRangeMarkation(observanceObject)
            markationResults.append(observanceObject)
        return markationResults

    def stockChronologicalLocationIdentifier(self, stockList):
        # Chron [stock, index]
        chronStart = self.calculateStockIndexToMarkate(stockList, self.chronIdentifierStartList)
        chronBeginWatch = self.calculateStockIndexToMarkate(stockList, self.chronIdentifierBeginWatchList)
        chronEndWatch = self.calculateStockIndexToMarkate(stockList, self.chronIdentifierEndWatchList)
        results ={"chronStart":chronStart,"chronBeginWatch":chronBeginWatch,"chronEndWatch":chronEndWatch}
        return results

    def calculateStockIndexToMarkate(self, stockList, chronListToFind):
        # From start interate every 10 minutes
        index = 0
        for stock in stockList:
            if(stock["hour_created"] == (chronListToFind[0])):
                if(stock["minute_created"] == chronListToFind[1]):
                    return [stock,index]
            index += 1

    def calculateWinOrLoseFullRange(self, observanceObject):
        fullRangeSet = observanceObject.getFullRangeSet()
        # print(observanceObject.getBoughtBidPrice())
        # print(observanceObject.getHighDelimiter())
        stockYieldHighPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getHighDelimiter()))
        stockYieldLowPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getLowDelimiter()))

        stockYieldHighPrice = (float(observanceObject.getBoughtBidPrice()) + stockYieldHighPriceVector)
        stockYieldLowPrice = (float(observanceObject.getBoughtBidPrice()) - stockYieldLowPriceVector)

        # print("stock purchase price: " + str(observanceObject.getBoughtBidPrice()))
        # print("stock yield high price: "+str(stockYieldHighPrice))
        # print("stock yield low price: " + str(stockYieldLowPrice))

        # print(len(markationSet))
        index = 0
        indexInternalSet = 0
        for stock in fullRangeSet:
            # print(float(stock["ask"]))
            # print("high "+ str(stockYieldHighPrice))
            # print("low " + str(stockYieldLowPrice))
            if (float(stock["ask"]) >= stockYieldHighPrice):
                # print("hit ask high")
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())
                # print(stock["ask"])

                observanceObject.setScenarioOutcome({
                "symbol":stock["symbol"],
                "outcome": 1,
                "boughtPrice": observanceObject.getBoughtBidPrice(),
                "ask": stock["ask"],
                "stockIndex": index,
                "percentageDifference":percentageDifference,
                "indexInternalSet":indexInternalSet
                })

                break
            if (float(stock["ask"]) <= stockYieldLowPrice):
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 0,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

                break
            if (index == (len(fullRangeSet) - 1)):
                indexInternalSet += 1
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 3,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

            index += 1

    def calculateWinOrLoseMarkation(self, observanceObject):
        markationSet = observanceObject.getMarkationSet()
        # print(observanceObject.getBoughtBidPrice())
        # print(observanceObject.getHighDelimiter())
        stockYieldHighPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getHighDelimiter()))
        stockYieldLowPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getLowDelimiter()))

        stockYieldHighPrice = (float(observanceObject.getBoughtBidPrice()) + stockYieldHighPriceVector)
        stockYieldLowPrice = (float(observanceObject.getBoughtBidPrice()) - stockYieldLowPriceVector)

        # print("stock purchase price: " + str(observanceObject.getBoughtBidPrice()))
        # print("stock yield high price: "+str(stockYieldHighPrice))
        # print("stock yield low price: " + str(stockYieldLowPrice))

        # print(len(markationSet))
        index = 0
        indexInternalSet = 0
        for stock in markationSet:
            # print(float(stock["ask"]))
            # print("high "+ str(stockYieldHighPrice))
            # print("low " + str(stockYieldLowPrice))
            if (float(stock["ask"]) >= stockYieldHighPrice):
                # print("hit ask high")
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())
                # print(stock["ask"])

                observanceObject.setScenarioOutcome({
                "symbol":stock["symbol"],
                "outcome": 1,
                "boughtPrice": observanceObject.getBoughtBidPrice(),
                "ask": stock["ask"],
                "stockIndex": index,
                "percentageDifference":percentageDifference,
                "indexInternalSet":indexInternalSet
                })

                break
            if (float(stock["ask"]) <= stockYieldLowPrice):
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 0,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

                break
            if (index == (len(markationSet) - 1)):
                # print("no yield found at index: " + str(index))
                indexInternalSet += 1
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 3,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

                pass
            index += 1

    def calculateWinOrLoseFullRangeMarkation(self, observanceObject):
        markationSet = observanceObject.getMarkationSet()
        # print(observanceObject.getBoughtBidPrice())
        # print(observanceObject.getHighDelimiter())
        stockYieldHighPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getHighDelimiter()))
        stockYieldLowPriceVector = (
            float(observanceObject.getBoughtBidPrice()) * float(observanceObject.getLowDelimiter()))

        stockYieldHighPrice = (float(observanceObject.getBoughtBidPrice()) + stockYieldHighPriceVector)
        stockYieldLowPrice = (float(observanceObject.getBoughtBidPrice()) - stockYieldLowPriceVector)

        index = 0
        indexInternalSet = 0
        for stock in markationSet:
            # print(float(stock["ask"]))
            # print("high "+ str(stockYieldHighPrice))
            # print("low " + str(stockYieldLowPrice))
            if (float(stock["ask"]) >= stockYieldHighPrice):
                # print("hit ask high")
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(stock["ask"]) - float(observanceObject.getBoughtBidPrice())) / float(
                    observanceObject.getBoughtBidPrice())
                # print(stock["ask"])

                observanceObject.setScenarioOutcome({
                "symbol":stock["symbol"],
                "outcome": 1,
                "boughtPrice": observanceObject.getBoughtBidPrice(),
                "ask": stock["ask"],
                "stockIndex": index,
                "percentageDifference":percentageDifference,
                "indexInternalSet":indexInternalSet
                })

                break
            if (float(stock["ask"]) <= stockYieldLowPrice):
                # print("hit ask low")
                indexInternalSet += 1
                observanceObject.setAskSellPrice(stock["ask"])
                percentageDifference = (float(stock["ask"]) - float(observanceObject.getBoughtBidPrice())) / float(
                    observanceObject.getBoughtBidPrice())
                # print(stock["ask"])

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 0,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

                break
            if (index == (len(markationSet) - 1)):
                # print("no yield found at index: " + str(index))
                indexInternalSet += 1
                percentageDifference = (float(observanceObject.getBoughtBidPrice()) - float(stock["ask"])) / float(
                    observanceObject.getBoughtBidPrice())

                observanceObject.setScenarioOutcome({
                    "symbol": stock["symbol"],
                    "outcome": 3,
                    "boughtPrice": observanceObject.getBoughtBidPrice(),
                    "ask": stock["ask"],
                    "stockIndex": index,
                    "percentageDifference": percentageDifference,
                    "indexInternalSet": indexInternalSet
                })

                pass
            index += 1
    def generateObservanceObject(self):
        observanceObject = ObservanceObject()
