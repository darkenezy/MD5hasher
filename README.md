# MD5hasher
Web service to get md5 of any resourse on the Internet

## Requirements
* python 3.6+
* aiohttp
`pip install aiohttp==3.4.4`

## Usage
### Run the service

`python main.py`

### Methods description

#### submit

*POST* `http://localhost:8080/submit`

*params*:

* `url` - your file adress
* `email` - not implemented yet

*response*: {'id': '0478f7a9-9041-4470-8c39-f5f0da76cfbf'}

#### check

*GET* `http://localhost:8080/check`

*params*:

* `id` - unique uuid gain via __*submit*__ method

*response*:

__200__

* `status: running` - request is still in work
* `status: falied` - request was interrupted on server side
* `status: finished` - successfully finished, md5 hash and file url in response

__404__

* `error: id not found` - specified uuid was not found in base