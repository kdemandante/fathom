import base64
from typeform import Typeform
import requests

def get_list(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    tfClient = Typeform({insert key})

    forms = tfClient.forms.list()
    form_ids = []
    for form in forms['items']:
        form_ids += [form['id']]
    print(form_ids)

def get_list2(event, context):
    url = 'https://api.typeform.com/forms'
    headers = {'Authorization' : 'Bearer {insert key}'}
    r = requests.get(url, headers)
    print(r.json())
