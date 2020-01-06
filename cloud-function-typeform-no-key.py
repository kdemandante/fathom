import base64
from typeform import Typeform
import json
from google.cloud import storage

key =

tfClient = Typeform(key)

storage_client = storage.Client()
bucket = storage_client.get_bucket() #insert bucket name

def upload_data(data, blobName):
    blob = bucket.blob(blobName)
    blob.upload_from_string(data, content_type='application/x-ndjson')

def get_forms():
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    forms = tfClient.forms.list(pageSize = 200)
    form_ids = []
    for form in forms['items']:
        form_ids += [form['id']]
        blobName = 'typeform/forms/' + form['id'] + '.'
        upload_data(json.dumps(tfClient.forms.get(form['id'])), blobName)
    return form_ids

def get_responses():
    formIds = get_forms()
    for id in formIds:
        response_form = tfClient.responses.list(id)
        response_list = response_form['items']
        responses = [json.dumps(response) for response in response_list]
        response_file = '\n'.join(responses)
        blobName = 'typeform/responses/' + id + '.ndjson'
        upload_data(response_file, blobName)

def main(event, context):
    get_responses()

if __name__ == "__main__":
    main()
