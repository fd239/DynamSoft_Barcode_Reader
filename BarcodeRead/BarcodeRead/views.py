import os
import sys
import cv2
import json
import base64
from typing import List
from dbr import *
import tempfile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

license_key = 't0068NQAAAJzD9TiccwrG0vlPSZJu3XY6KmgpuX6aky5RF0rNgRv0biYGPQQpmrMqpVLxQyP6tc3aNC0Pz88mQWxlt5wK4mY='
license_server = ''

@csrf_exempt
def read_barcode(request):
    
    result = []

    if request.method == 'POST':
        decoded_body = request.body.decode('utf-8')
        dict_list = json.loads(decoded_body.lstrip('\ufeff'))

    for dict_item in dict_list:
        encoded_image = base64.b64decode(dict_item['Image'])
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(encoded_image)
            file_name = tmp.name 

    reader = BarcodeReader()
    reader.init_license(license_key)

    try:
        text_results = reader.decode_file(file_name)
        if text_results != None:
            for text_result in text_results:
                result.append({'barcodeFormatString':text_result.barcode_format_string, 'barcodeText': text_result.barcode_text})
   
    except BarcodeReaderError as bre:
        print(bre)

    try:
        os.remove(file_name)    
    except:
        print(Exception)

    return HttpResponse(json.dumps(result, sort_keys=True, indent=4), content_type='application/json')

def it_works(request):
    return HttpResponse('It works!', content_type='text/plain')        