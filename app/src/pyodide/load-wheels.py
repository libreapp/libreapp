# pylint: disable=import-error

import importlib
import io
import json
from pathlib import Path
import zipfile

from js import Promise, XMLHttpRequest

WHEEL_BASE_PATH = Path('/lib/python3.7/site-packages/').parent
VENDOR_WHEEL_BASE_URL = '/vendor/wheels/'
VENDOR_WHEEL_INDEX_FILENAME = 'index.json'
VENDOR_WHEEL_INDEX_URL = '{}{}'.format(
    VENDOR_WHEEL_BASE_URL, VENDOR_WHEEL_INDEX_FILENAME)


def _nullop(*args):
    return


def get_url(url):
    def run_promise(resolve, reject):
        def callback(data):
            resolve(data)

        _get_url_async(url, callback)

    return Promise.new(run_promise)


def _get_url_async(url, cb):
    req = XMLHttpRequest.new()
    req.open('GET', url, True)
    req.responseType = 'arraybuffer'

    def callback(e):
        if req.readyState == 4:
            cb(io.BytesIO(req.response))

    req.onreadystatechange = callback
    req.send(None)


def extract_wheel(fd):
    with zipfile.ZipFile(fd) as zf:
        zf.extractall(WHEEL_BASE_PATH)

    importlib.invalidate_caches()


def get_package(url):
    def do_install(resolve, reject):
        def run_promise(wheel):
            try:
                extract_wheel(wheel)
            except Exception as e:
                reject(str(e))
            else:
                resolve()

        get_url(url).then(run_promise)
        importlib.invalidate_caches()

    return Promise.new(do_install)


def load_and_copy_wheels(base_url, index_url):
    def run_promise(resolve, reject):
        def extract_all_wheels(wheel_index_json):
            wheel_index = json.load(wheel_index_json)

            for wheel in wheel_index:
                wheel_name = wheel.split('/')[-1].split('-')[0]
                print('Loading {} from python-wheels'.format(wheel_name))

            urls = [
                '{}{}'.format(base_url, wheel)
                for wheel in wheel_index]

            promises = []
            for url in urls:
                promises.append(get_package(url))

            Promise.all(promises).then(resolve)

        get_url(index_url).then(extract_all_wheels)

    return Promise.new(run_promise)


Promise.all([
    load_and_copy_wheels(VENDOR_WHEEL_BASE_URL, VENDOR_WHEEL_INDEX_URL)
])
