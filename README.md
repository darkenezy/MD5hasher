# MD5hasher
Web service to get md5 of any resourse on the Internet

## Requirements
* python 3.6+
* aiohttp
`pip install aiohttp`

## Usage
### Run the service
`python3 <path>\main.py`
### Methods description
*POST* `http://localhost:8080/submit`
*params*:
`url` - your file adress
`email` - not implemented yet
*response*:
{'id': <unique uuid>}

*GET* `http://localhost:8080/submit`
*params*:
`id` - unique uuid gain via __*submit*__ method
*response*:
__200__
`status: running` - request is still in work
`status: falied` - request was interrupted on server side
`status: finished` - successfully finished, md5 hash and file url in response
__404__
`error: id not found` - specified uuid was not found in base





