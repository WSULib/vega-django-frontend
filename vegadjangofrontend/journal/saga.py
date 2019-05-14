# Saga Client and GROQ Querying

import requests
import json


class SagaClient(object):
    '''
    Client to connect with Saga backend
    '''

    def __init__(self, host=None, port=None, dataset=None):
        '''
        Args:
            host (str): host
            port (int): port number
            dataset (str): dataset, likely ending with `--pub`
        '''

        self.host = host
        self.port = port
        self.dataset = dataset

    def identify(self):
        '''
        Saga identification
        '''

        return requests.get('http://%s:%s' % (self.host, self.port)).json()

    def groq_query(self, query):
        '''
        Issue query as POST request

        Args:
            query (str): GROQ query string
                - handles multi-line strings
        '''

        # prepare query
        query_json = json.dumps({
            'query': query
        })
        print(query_json)

        # issue request
        r = requests.post(
            'http://%s:%s/v1/data/query/%s' % (self.host, self.port, self.dataset),
            data=query_json,
            headers={
                'Content-Type': 'application/json'
            }
        )

        # return
        return r.json()
