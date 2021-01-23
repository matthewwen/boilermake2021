import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
endpoint_url = "http://api.nessieisreal.com"
api_key = os.getenv('CAPITAL_ONE_API_KEY')


def process_request(url, payload):
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={'content-type': 'application/json', "Accept": "application/json"}
    )
    return response is not None and response.status_code == 201, response


def create_content(response):
    if response.status_code == 201:
        my_json = response.content.decode('utf8').replace("'", '"')
        return json.loads(my_json)
    return None


class Nessie:

    def __init__(self, customer_id, account_id):
        self.customer_id = customer_id
        self.account_id = account_id

    def create_customer(self):
        url = endpoint_url + f"/customers?key={api_key}"
        payload = {
            "first_name": "Purdue",
            "last_name": "Pete",
            "address": {
                "street_number": "610",
                "street_name": "Purdue Mall",
                "city": "West Lafayette",
                "state": "IN",
                "zip": "47907"
            }
        }
        is_valid, response = process_request(url, payload)
        content = create_content(response)
        self.customer_id = content['objectCreated']['_id'] if is_valid else None
        return self.customer_id is not None

    def create_account(self):
        if self.customer_id is not None:
            url = endpoint_url + f"/customers/{self.customer_id}/accounts?key={api_key}"
            payload = {
                'type': 'Checking',
                'nickname': 'Boilermake',
                'rewards': 10000,
                'balance': 10000,
            }
            is_valid, response = process_request(url, payload)
            content = create_content(response)
            self.account_id = content['objectCreated']['_id'] if is_valid else None
            return is_valid
        return False
