import requests
import time
import asyncio
import traceback
import os

ADMIN_USERNAME = os.getenv("ADMINUSERNAME", "RICKASTLEY")
ADMIN_PASSWORD = os.getenv("ADMINPASSWORD", "GIVEYOUUPNEVERGONNA")
USERAGENT = os.getenv("USERAGENT", "Admins User Agent - Never Gonna Give You Up, Never Gonna Let You Down")

API_ROOT = os.getenv("APIROOT", "http://127.0.0.1:8080")

GET_FLAG_WAIT = int(os.getenv("GETFLAGWAIT", "1"))

# async def main():
#     print("Launching browser")
#     browser = await launch()
#     print("Launched browser")
#     page = await browser.newPage()
    
#     await page.setUserAgent(USERAGENT)
    
#     await page.goto(f'{API_ROOT}/')
#     script = '''async () => {
#         let a = await fetch("''' + API_ROOT + '''/api/login", {
#             method: "POST",
#             headers: {
#                 "Accept":"application/json, text/plain, */*",
#                 'Content-Type': 'application/json;charset=UTF-8',
#                 "sec-fetch-dest": "empty",
#                 "sec-fetch-mode": "cors",
#                 "sec-fetch-site": "same-origin"
#             },
#             "credentials":"include",
#             "mode":"cors",
#             body: `{"username":"''' + ADMIN_USERNAME + '''","password":"''' + ADMIN_PASSWORD + '''"}`
#         })
#         return await a.json()
#     }'''
#     login = await page.evaluate(script)
#     print(login)
#     await page.goto(f'{API_ROOT}/api/flag')
#     print(await page.content())
#     await browser.close()

async def readflag():
    print("Sending request")
    s = requests.Session()
    s.post(f'{API_ROOT}/api/login', json={
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
    }, headers={
        "User-Agent": USERAGENT
    })

    r = s.get(f'{API_ROOT}/api/flag')
    print(r.json())


while True:
    try:
        print("Start")
        asyncio.get_event_loop().run_until_complete(readflag())
        print("Finish")
    except:
        traceback.print_exc()
        pass
    time.sleep(GET_FLAG_WAIT*60)
