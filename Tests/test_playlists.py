import json
import unittest
import jsonschema
import pytest

import os
import sys

# Obtém o diretório raiz do projeto
diretorio_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(diretorio_raiz)

from Requests.request_oauth2 import MyOauth2
from Requests.requests import Requests
from Resources import utils as Utils


class PLaylists(unittest.TestCase):

    def setUp(self):
        self.data = Utils.load_json_file("data.json")

        oauth2 = MyOauth2()
        self.token = oauth2.access_token_get(self.data["client_id"],
                                             self.data["client_secret"],
                                             self.data["scope"],
                                             self.data["callback_uri"],
                                             self.data["token"])
        self.access_token = self.token["access_token"]
        self.request = Requests()

    def test_get_playlists(self):
        response = self.request.playlists_get(self.access_token, '22qezhjglgsamssh45nnfdexy')
        assert response.status_code == 200

        try:
            playlists_schema = Utils.load_schema_file("playlists_schema.json")
            jsonschema.validate(json.loads(response.text), playlists_schema)
        except:
            pytest.fail("JSON file received doesn't have the expected format \n", False)

    def test_get_playlists_fail(self):
        response = self.request.playlists_get(self.access_token, '22qezhjglgsamssh45nnfdexy')
        assert response.status_code == 200

        try:
            playlists_schema = Utils.load_schema_file("playlists_schema_fail.json")
            jsonschema.validate(json.loads(response.text), playlists_schema)
        except:
            pytest.fail("JSON file received doesn't have the expected format \n", False)

    # def test_create_new_playlist(self):
    #     body = {
    #         "name": "Playlist test code",
    #         "description": "Essa playlist foi criada via python requests",
    #         "public": False
    #     }
    #
    #     response = self.request.playslist_create(self.access_token, '22qezhjglgsamssh45nnfdexy', body)
    #     assert response.status_code == 201

    def tearDown(self):
        self.data['token'] = self.token
        Utils.update_json_file('data.json', self.data)