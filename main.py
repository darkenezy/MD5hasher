from uuid import uuid4
from aiohttp import web, ClientSession

from hash_request import *


host = 'localhost'
port = '8080'

storage = {
    "session": None,
    "futures": []
} # ToDo: change for db

async def init_session():
    storage["session"] = ClientSession()

# /submit
async def submit(request):
    url = request.query.get("url")
    email = request.query.get("email")
    
    uuid = str(uuid4())
    storage[uuid] = HashRequest(url, storage)
    
    return web.json_response({"id": uuid})

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

if __name__ == "__main__":
    try:
        runner = web.AppRunner(app)
        loop.run_until_complete(init_session())
        loop.run_until_complete(runner.setup())
        
        site = web.TCPSite(runner, '0.0.0.0', 80)
        loop.run_until_complete(site.start())

        print("[Server running on http://0.0.0.0:80]")
        loop.run_forever()
        
    except KeyboardInterrupt:
        print("Fininshing...")
        loop.run_until_complete(storage["session"].close())
        loop.run_until_complete(asyncio.gather(*storage["futures"]))
        
    except Exception as e:
        print(e)
        
    finally:
        loop.close()
                                
