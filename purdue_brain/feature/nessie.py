import json

import requests

endpoint_url = "http://api.nessieisreal.com"


def process_request(url, payload):
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={'content-type': 'application/json', "Accept": "application/json"}
    )
    return response is not None and response.status_code == 201


class Nessie:

    def __init__(self, customer_id, api_key):
        self.customer_id = customer_id
        self.api_key = api_key

    def create_customer(self):
        url = endpoint_url + f"/customers?key={self.api_key}"
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
        return process_request(url, payload)

    def create_account(self):
        url = endpoint_url + f"/customers/{self.customer_id}/accounts?key={self.api_key}"
        payload = {
            'type': 'Debit Card',
            'nickname': 'Boilermake',
            'balance': 10000,
        }
        return process_request(url, payload)
