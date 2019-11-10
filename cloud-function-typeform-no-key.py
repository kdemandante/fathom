import base64
from typeform import Typeform
import json
from google.cloud import storage

key =

tfClient = Typeform(key)

storage_client = storage.Client()
bucket = storage_client.get_bucket('fathom_data_lake')

def get_list():
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    forms = tfClient.forms.list(pageSize = 200)
    form_ids = []
    for form in forms['items']:
        form_ids += [form['id']]
    return form_ids

def upload_response(response, blobName):
    blob = bucket.blob(blobName)
    blob.upload_from_string(json.dumps(response), content_type='application/json')

def get_responses(event, context):
    formIds = get_list()

    for id in formIds:
        responses = tfClient.responses.list(id)
        for response in responses['items']:
            blobName = 'typeform/' + response['submitted_at'].replace('-', '/')[:10] + '/' + response['response_id']
            upload_response(response, blobName)
            #tfClient.responses.delete(id, response['token'])
            break
        break
