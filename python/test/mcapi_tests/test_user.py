import unittest
from mcapi import set_remote_config_url, get_all_users

url = 'http://mctest.localhost/api'

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        set_remote_config_url(url)

    def test_get_all(self):
        print ''

        my_id = "test@test.mc"
        me = None
        user_list = get_all_users()

        print user_list

        for user in user_list:
            if (user.id == my_id):
                me = user
        print user.input_data
        self.assertIsNotNone(me)
        self.assertEqual(me.fullname,"Test User1")

        another_id = "another@test.mc"
        another = None
        for user in user_list:
            if (user.id == another_id):
                another = user
        self.assertIsNotNone(another)
        self.assertEqual(another.fullname,"Test User2")

