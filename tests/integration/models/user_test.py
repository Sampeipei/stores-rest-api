from tests.base_test import BaseTest
from models.user import UserModel


class UserModelTest(BaseTest):
    def test_crud(self):
        with self.app_context():            
            user = UserModel("test user", "dummy passwrod")
            self.assertIsNone(UserModel.find_by_username("test user"))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username("test user"))
            self.assertIsNotNone(UserModel.find_by_id(1))
            user_searched = UserModel.find_by_username("test user")
            self.assertEqual("test user", user_searched.username)
            self.assertEqual("dummy passwrod", user_searched.password)
