from tests.unit.unite_base_test import UniteBaseTest
from models.user import UserModel
import unittest


class UserModelTest(unittest.TestCase):
    def test_create_user(self):
        user = UserModel("user name", "passwordddd")
        self.assertEqual("user name", user.username)
        self.assertEqual("passwordddd", user.password)
