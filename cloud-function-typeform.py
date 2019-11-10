import base64
from typeform import Typeform
import json
from google.cloud import storage

key = 'DTcQuGKoY746VUN48KbTGASnvZ9k3R5kFnKi7Z9HN1QT'

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

{'total_items': 2, 'page_count': 1, 'items': [{'landing_id': 'j12oesu4awl8s9zej12ompzc0g6e7nvf', 'token': 'j12oesu4awl8s9zej12ompzc0g6e7nvf', 'response_id': 'j12oesu4awl8s9zej12ompzc0g6e7nvf', 'landed_at': '2019-11-04T03:23:52Z', 'submitted_at': '2019-11-04T03:24:03Z', 'metadata': {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36', 'platform': 'other', 'referer': 'https://fathompbc.typeform.com/to/RB0DqR?typeform-embed=embed-widget&embed-opacity=100&typeform-embed-id=owxby', 'network_id': '98ad56b766', 'browser': 'default'}, 'answers': [{'field': {'id': 'Jdzz8My1Fmnz', 'type': 'email', 'ref': '6648fdbc-2d5c-4257-bcdd-b329bd26539d'}, 'type': 'email', 'email': 'nick.lorenson@corrdyn.com'}, {'field': {'id': 'NfsOP7MaSI31', 'type': 'multiple_choice', 'ref': '534a76db-399e-4a87-8ae8-0256bc077f73'}, 'type': 'choice', 'choice': {'label': 'first choice'}}]},
{'landing_id': 'xr71i8ud8j8m48hxr71wdm04tdbp3npz', 'token': 'xr71i8ud8j8m48hxr71wdm04tdbp3npz', 'response_id': 'xr71i8ud8j8m48hxr71wdm04tdbp3npz', 'landed_at': '2019-11-04T03:27:20Z', 'submitted_at': '0001-01-01T00:00:00Z', 'metadata': {'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36', 'platform': 'other', 'referer': 'https://fathompbc.typeform.com/to/RB0DqR?typeform-embed=embed-widget&embed-opacity=100&typeform-embed-id=9kug2', 'network_id': '98ad56b766', 'browser': 'default'}, 'answers': None}]}
