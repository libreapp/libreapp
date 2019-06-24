import urllib.request


FILES_TO_DOWNLOAD = [
    {
        "url": 'https://github.com/iodide-project/pyodide/releases/download/0.13.0/pyodide-build-0.13.0.tar.bz2',
        "hash": 'd8bb9ec31c87d80bcc4ed9f1477289b679b03ba4a082ebddde88f9416a92376a',
        "location": '.',
        "extract": True
    },
    {
        "url": 'https://files.pythonhosted.org/packages/97/ae/93aeb6ba65cf976a23e735e9d32b0d1ffa2797c418f7161300be2ec1f1dd/pydicom-1.2.0-py2.py3-none-any.whl',
        "hash": '2132a9b15a927a1c35a757c0bdef30c373c89cc999cf901633dcd0e8bdd22e84',
        "location": 'wheels',
        "extract": False
    }
]


# TODO call this function on `yarn bootstrap`
def main():

    for item in FILES_TO_DOWNLOAD:
        urllib.request.urlretrieve(item['url'])
        # TODO check hash
        # TODO move to defined location
        # TODO extract
