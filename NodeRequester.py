import aiohttp
import asyncio
from threading import Thread
import json as JSON
import requests


class NodeRequester:
    def __init__(self):
        self.list_chosen_data_managers = []
        self.chosen_stock_temp_container = []

    def getAllRecordSets(self, date):
        response = self.postRequest(
            {
                "request_type": "neocortex",
                "isGetAllDaysByDate": 1,
                "date": date
            })
        return response

    def getGoldenGooseMetrics(self):
        # response = self.postRequest(
        #     {
        #         "request_type": "neocortex",
        #         "isGetAllDaysByDate": 1,
        #         "date": date
        #     })
        response = {
            "data": {
                "highPriceDelimiter": 14,
                "lowPriceDelimiter": 5
            }
        }
        return response

    def postGoldenGooseResult(self, isChosenDetermined, listPrioritizedGeeseMetrics):
        json = {
                "request_type": "intakeGoldenGooseResultStore",
                "isChosenDetermined": isChosenDetermined,
                "listPrioritizedGeeseMetrics": listPrioritizedGeeseMetrics
            }
        print("JSON: "+str(json))

        response = self.postRequest(
            json
        )
        return response

    def postBuyBreachWatch(self):
        json = {
                "request_type": "breachWatchBuy"
            }
        response = self.postRequest(
            json
        )
        return response
#



    def postRequest(self, jsonData):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            self.async_post_neocortex(
                jsonData))
        jsonResponse = JSON.loads(response)
        return jsonResponse

    async def fetch(self, session, url, data):
        async with session.post(url, data=data) as response:
            return await response.text()

    async def async_post_neocortex(self, request):
        async with aiohttp.ClientSession() as session:
            url = 'http://localhost:3000/api/brokerage'
            response_returned = await self.fetch(session, url, request)
            return response_returned
