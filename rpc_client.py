""" Async Solana JSON RPC calls """

import asyncio
import json
import aiohttp
import requests

from dotenv import dotenv_values


variables = dotenv_values(".env")

node = requests.get(variables["RPC"])

url = node.text

text = json.loads(url)

RPC = str(text["node"])


async def fetch(data):


    """ Posts data for RPC calls, returns response in JSON. """


    count = 0


    while True:


        try:


            async with aiohttp.ClientSession() as session:


                async with session.post(RPC, json=data) as resp:


                    response = await resp.json()

                    await session.close()


        except: # pylint: disable=W0702


            print("\nError fetching data")

            print("\nSleeping for 10 seconds")

            await asyncio.sleep(10)

            count += 1


            if count == 10:


                return None 


        else:


            break


    return response


async def account_signatures(address):


    """ https://docs.solana.com/developing/clients/jsonrpc-api#getsignaturesforaddress """


    data = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [address, {"limit":1000}]

            }


    response = await fetch(data)

    signatures = []


    for i in range(0, len(response["result"])):


        signatures.append(response["result"][i]["signature"])


    return signatures


async def search(until, address):


    """ https://docs.solana.com/developing/clients/jsonrpc-api#getsignaturesforaddress """


    data = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [address, {"until": until}]

            }


    response = await fetch(data)

    signatures = []


    for i in range(0, len(response["result"])):


        signatures.append(response["result"][i]["signature"])


    return signatures


async def transaction_details(signature):


    """ https://docs.solana.com/developing/clients/jsonrpc-api#gettransaction """


    data = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature]
            #"json": ""

            }


    details = await fetch(data)


    return details


async def get_account_info(account):


    """ https://docs.solana.com/developing/clients/jsonrpc-api#getaccountinfo """


    data = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [account, {"encoding": "base64"}]

            }


    account_info = await fetch(data)


    return account_info


async def performance_metrics():


    """ https://docs.solana.com/developing/clients/jsonrpc-api#getrecentperformancesamples """


    data = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getRecentPerformanceSamples",
            "params": [1]

            }


    response = await fetch(data)


    return response
