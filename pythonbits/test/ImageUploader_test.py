import re
import json

import responses
from nose.tools import raises

from pythonbits.ImageUploader import upload, BASE_URL, BaconBitsImageUploadError


@responses.activate
def test_upload_from_url_returns_valid_url():

    def response_json_callback(request):
        return (200,
                {},
                json.dumps({'ImgName': 'image.jpg'}))

    responses.add_callback(responses.POST,
                           'https://images.baconbits.org/upload.php',
                           callback=response_json_callback,
                           content_type='application/json')

    s = upload('http://example.com/image.jpg')
    assert s == 'https://images.baconbits.org/images/image.jpg'


@raises(BaconBitsImageUploadError)
@responses.activate
def test_no_json_or_bad_response_raises_err():
    def response_json_callback(request):
        return (404,
                {})

    responses.add_callback(responses.POST,
                           'https://images.baconbits.org/upload.php',
                           callback=response_json_callback,
                           content_type='application/json')

    upload('http://example.com/image.jpg')


@raises(BaconBitsImageUploadError)
@responses.activate
def test_missing_key_raises_err():

    def response_json_callback(request):
        return (200,
                {},
                json.dumps({'error': 'badly!'}))

    responses.add_callback(responses.POST,
                           'https://images.baconbits.org/upload.php',
                           callback=response_json_callback,
                           content_type='application/json')

    upload('http://example.com/image.jpg')
