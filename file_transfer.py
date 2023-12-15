from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ImagesApi()
body = swagger_client.ImagesUploadBody() # ImagesUploadBody |

try:
    # Upload an image for AI processing.
    api_response = api_instance.upload_image(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ImagesApi->upload_image: %s\n" % e)
