import asyncio
from hashlib import md5


class HashRequest():
    def __init__(self, url, email=None):
        self._url = url
        self._email = email
        
        self._status = "running"
        self._hash = md5()

        coroutine = asyncio.ensure_future(self.get_file())
        storage["futures"].append(coroutine)

    def get_json(self):
        res = {
            "status": self._status
        }

        if self._status == "done":
            res["url"] = self._url
            res["md5"] = self._hash.hexdigest()
            
        return res
            

    async def get_file(self):
        try:
            async with storage["session"].get(self._url) as resp:
                if resp.status == 404:
                    self._status = "failed"

                while True:
                    chunk = await resp.content.read(524288)
                    if not chunk:
                        break
                    self._hash.update(chunk)
                    
                self._status = "done"
                if self.email:
                    pass #ToDo: send email? async lib needed

        except Exception as e:
            self._status = "failed"
