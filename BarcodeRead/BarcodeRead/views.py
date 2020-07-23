import base64
import cv2
import os
import sys
import json
import tempfile

from dbr import *
from dotenv import load_dotenv
from typing import List

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

load_dotenv()

LICENSE_KEY = os.getenv('LICENSE_KEY')
LICENSE_CONTENT = os.getenv('LICENSE_CONTENT')


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_barcode(request):

    result = []

    decoded_body = request.body.decode('utf-8')
    dict_list = json.loads(decoded_body.lstrip('\ufeff'))

    for dict_item in dict_list:
        encoded_image = base64.b64decode(dict_item['Image'])
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(encoded_image)
            file_name = tmp.name

    reader = BarcodeReader()
    reader.init_license_from_license_content(LICENSE_KEY, LICENSE_CONTENT)

    try:
        text_results = reader.decode_file(file_name)
        if text_results != None:
            for text_result in text_results:
                result.append({'barcodeFormatString': text_result.barcode_format_string,
                               'barcodeText': text_result.barcode_text})
    except BarcodeReaderError as bre:
        return Response(f'Barcode reader error :[{bre}]', status=status.HTTP_400_BAD_REQUEST)

    try:
        os.remove(file_name)
    except:
        return Response(f'Error deleting files :[{Exception}]', status=status.HTTP_400_BAD_REQUEST)

    return Response(data=result, status=status.HTTP_200_OK)
