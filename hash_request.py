import asyncio     
from hashlib import md5
from email.mime.text import MIMEText


class HashRequest():
    def __init__(self, url, storage, email):
        self._url = url
        self._email = email
            
        self._status = "running"
        self.storage = storage
        self._hash = None

        coroutine = asyncio.ensure_future(self.get_hash())
        storage["futures"].append(coroutine)

    def get_json(self):
        res = {
            "status": self._status
        }

        if self._status == "done":
            res["url"] = self._url
            res["md5"] = self._hash.hexdigest()
            
        return res
            

    async def get_hash(self):
        self._hash = md5()
        try:
            async with self.storage["session"].get(self._url) as resp:
                if resp.status == 404:
                    self._status = "failed"
                else:
                    while True:
                        chunk = await resp.content.read(524288)
                        if not chunk:
                            break
                        self._hash.update(chunk)
                        
                    self._status = "done"

                    if self._email:
                        asyncio.ensure_future(self.send_email())
                        
        except Exception as e:
            self._status = "failed"
            
    async def send_email(self):
        answer = "url: {}\nmd5: {}".format(self._url, self._hash.hexdigest())
        
        message = MIMEText(answer)
        message["To"] = self._email
        message["Subject"] = "MD5hasher - results"
        
        await self.storage["smtp"].send_message(message)
        
