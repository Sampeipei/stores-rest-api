from werkzeug.datastructures import iter_multi_items
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        # Make sure to call setup method in super class
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("test_user", "test_password").save_to_db()
                # Authorize
                auth_res = client.post(
                    "/auth", 
                    data=json.dumps(
                        {"username":"test_user", "password": "test_password"}),
                    headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_res.data)["access_token"]
                self.access_token = "JWT " + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                res = client.get("/item/test")
                expected = {
                    "message": "Could not authorize. Did you include a valid Authorization header?"
                }
                self.assertEqual(res.status_code, 401)
                self.assertDictEqual(json.loads(res.data), expected)

    def test_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Get item resource
                item_res = client.get(
                    "/item/test",
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 404)
                self.assertDictEqual(
                    json.loads(item_res.data),
                    {'message': 'Item not found'}
                )

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                ItemModel("Google pixel", 699.99, 1).save_to_db()
                # Get item resource
                item_res = client.get(
                    "/item/Google pixel",
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 200)
                self.assertDictEqual(
                    json.loads(item_res.data),
                    {'name': 'Google pixel', "price": 699.99}
                )

    def test_create_single_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Get item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 699.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Google pixel"))

    def test_create_multiple_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Create item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 699.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Google pixel"))

                # Create different item resource
                item_res = client.post(
                    "/item/Chrome book",
                    data={"price": 999.99, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Chrome book"))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Create item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 699.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Google pixel"))

                # Create duplicate item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 109.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 400)
                self.assertDictEqual(
                    {'message': "An item with name 'Google pixel' already exists."},
                    json.loads(item_res.data)
                )

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Create item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 699.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("Google pixel"))

                # Delete item
                item_res = client.delete("/item/Google pixel")
                self.assertEqual(item_res.status_code, 200)
                self.assertDictEqual(
                    json.loads(item_res.data),
                    {'message': 'Item deleted'})
                self.assertIsNone(ItemModel.find_by_name("Google pixel"))

    def test_put_exsisting_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Create item resource
                item_res = client.post(
                    "/item/Google pixel",
                    data={"price": 699.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertIsNotNone(ItemModel.find_by_name("Google pixel"))

                # Update existing item
                item_res = client.put(
                    "/item/Google pixel",
                    data={"price": 0.9, "store_id": 2},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 200)
                self.assertDictEqual(
                    {"name": "Google pixel", "price": 0.9},
                    json.loads(item_res.data)
                )
                updated_item = ItemModel.find_by_name("Google pixel")
                self.assertEqual(updated_item.name, "Google pixel")
                self.assertEqual(updated_item.price, 0.9)
                self.assertEqual(updated_item.store_id, 1)
                
    def test_put_new_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                # Update new item
                self.assertIsNone(ItemModel.find_by_name("Google pixel"))
                item_res = client.put(
                    "/item/Google pixel",
                    data={"price": 0.9, "store_id": 1},
                    headers={"Authorization": self.access_token})
                self.assertEqual(item_res.status_code, 200)
                self.assertDictEqual(
                    {"name": "Google pixel", "price": 0.9},
                    json.loads(item_res.data)
                )
                updated_item = ItemModel.find_by_name("Google pixel")
                self.assertIsNotNone(updated_item)
                self.assertEqual(updated_item.name, "Google pixel")
                self.assertEqual(updated_item.price, 0.9)
                self.assertEqual(updated_item.store_id, 1)

    def test_get_empty_item_list(self):
        with self.app() as client:
            with self.app_context():
                res = client.get("/items")
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual(
                    json.loads(res.data),
                    {
                        "items": []
                    }
                )

    def test_get_item_list_with_single_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                ItemModel("Google pixel", 699.99, 1).save_to_db()
                res = client.get("/items")
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual(
                    json.loads(res.data),
                    {
                        "items": [
                            {"name": "Google pixel", "price": 699.99}
                        ]
                    }
                )

    def test_get_item_list_with_mulitple_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Google store").save_to_db()
                ItemModel("Google pixel", 699.99, 1).save_to_db()
                ItemModel("Chrome book", 999.9, 1).save_to_db()
                res = client.get("/items")
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual(
                    json.loads(res.data),
                    {
                        "items": [
                            {"name": "Google pixel", "price": 699.99},
                            {"name": "Chrome book", "price": 999.9}
                        ]
                    }
                )
