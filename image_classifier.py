"""
The Clarifai API will be used to help us identify what's going on in the picture by setting
a tag and a prediction value of how likely the associated tag is true to the picture.
"""

import os
from decouple import config
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

# load_dotenv()

CLARIFAI_API_KEY=config("CLARIFAI_API_KEY")
# CLARIFAI_API_KEY = os.environ.get('CLARIFAI_API_KEY')
metadata = (('authorization', CLARIFAI_API_KEY),)

def get_tags(image_url):
    """
    Makes a request to the Clarifai API to analyze the picture sent in through WhatsApp.
    """
    relevant_tags = {}
    request = service_pb2.PostModelOutputsRequest(
      model_id='aaa03c23b3724a16a56b629203edc62c',
      inputs=[
        resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=image_url)))
    ])
    response = stub.PostModelOutputs(request, metadata=metadata)
    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))
    for concept in response.outputs[0].data.concepts:
        print('%12s: %.2f' % (concept.name, concept.value), "\n")
        relevant_tags[concept.name] = round(concept.value, 2)
    return relevant_tags
