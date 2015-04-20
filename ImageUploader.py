#!/usr/bin/env python
# encoding: utf-8
"""
ImageUploader.py

Created by Ichabond on 2012-07-01.
"""

import requests


BASE_URL = 'https://images.baconbits.org/'


class BaconBitsImageUploadError(Exception):
    pass


def upload(file_or_url):
    if any(file_or_url.startswith(schema) for schema in
           ('http://', 'https://')):
        files = {'url': file_or_url}
    else:
        files = {'ImageUp': open(file_or_url, 'rb')}

    try:
        j = requests.post(BASE_URL + 'upload.php',
                          files=files).json()
    except ValueError:
        raise BaconBitsImageUploadError("Failed to upload '%s'!" % file_or_url)

    if 'ImgName' in j:
        return BASE_URL + 'images/' + j['ImgName']
    else:
        raise BaconBitsImageUploadError("Failed to upload '%s'!" % file_or_url,
                                        repr(j))
