import aiosmtplib
from aiohttp import web, ClientSession, MultipartReader

import json
from uuid import uuid4

from hash_request import *


host = 'localhost'
port = '8080'

with open("config.json", encoding="utf-8") as fp:
    creds = json.loads(fp.read())
        
storage = {
    "session": None,
    "futures": [],
    "smtp": None
} # ToDo: change for db

async def init_session():
    storage["session"] = ClientSession()

# /submit
async def submit(request):
    if request.content_type == "application/json":
        json = await request.json()

        # Retrieve url
        url = json.get("url")
        if not url:
            return web.json_response({"error": "url is not specified"}, status=400)

        # Retrieve email
        email = json.get("email")

        uuid = str(uuid4())
        storage[uuid] = HashRequest(url, storage, email)
        
        return web.json_response({"id": uuid})
    
    return web.json_response({"error": "content type should be application/json"}, status=400)
        

# /check
async def check(request):
    _id = request.query.get("id")
    
    if not storage.get(_id):
        return web.json_response({"error": "id not found"}, status=404)   
        
    return web.json_response(storage[_id].get_json())

# Web application init
app = web.Application()
app.router.add_get('/check', check)
app.router.add_post('/submit', submit)

loop = asyncio.get_event_loop()
smtp = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=465, loop=loop, use_tls=True)

storage["smtp"] = smtp
loop.run_until_complete(smtp.connect())
loop.run_until_complete(smtp.login(username=creds["login"], password=creds["password"]))

if __name__ == "__main__":
    try:
        runner = web.AppRunner(app)
        loop.run_until_complete(init_session())
        loop.run_until_complete(runner.setup())
        
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        loop.run_until_complete(site.start())

        print("[Server running on http://0.0.0.0:8080]")
        loop.run_forever()
        
    except KeyboardInterrupt:
        print("Fininshing...")
        loop.run_until_complete(asyncio.gather(*storage["futures"]))
        loop.run_until_complete(storage["session"].close())
        
        
    except Exception as e:
        print(e)
        
    finally:
        loop.close()
                                
