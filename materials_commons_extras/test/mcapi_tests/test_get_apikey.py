import unittest
from materials_commons.api import get_apikey
import pytest
import requests


class TestGetApikey(unittest.TestCase):

    def test_get_valid_user(self):
        apikey = get_apikey("test@test.mc", "test")
        self.assertEqual(apikey, "totally-bogus")

    def test_get_invalid_user(self):
        with pytest.raises(requests.exceptions.HTTPError) as e:
            get_apikey("no-such-user@doesnot-exist.com", "bogus")
            self.assertEqual(e.response.status_code, 401)

    def test_wrong_password(self):
        with pytest.raises(requests.exceptions.HTTPError) as e:
            get_apikey("test@test.mc", "wrong-password")
            self.assertEqual(e.response.status_code, 401)

