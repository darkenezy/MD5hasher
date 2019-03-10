import asyncio     
from hashlib import md5


class HashRequest():
    def __init__(self, url, storage, email=None):
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
                    if self.email:
                        await self.send_email()
                        
        except Exception as e:
            self._status = "failed"
            
    async def send_email(self):
        # Google API Auth
        # https://developers.google.com/gmail/api/auth/web-server
        token = "TOKEN"
        url = 'https://www.googleapis.com/gmail/v1/users/{}/messages/send'.format(self.email)
        headers = {'Authorization':  'Bearer ' + token}

        # Creating message
        # See https://developers.google.com/gmail/api/guides/sending
        data = {'raw': 'msg_object'}
        await self.storage['session'].post(url, headers=headers, data=data)
        
