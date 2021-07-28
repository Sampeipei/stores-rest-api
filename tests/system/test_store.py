from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                res = client.post(
                    "/store/Google store")
                self.assertIsNotNone(StoreModel.find_by_name("Google store"))
                self.assertEqual(201, res.status_code)
                self.assertDictEqual(
                    {'name': "Google store", 'items': []},
                    json.loads(res.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Amazon store")
                res = client.post(
                    "/store/Amazon store")
                
                self.assertIsNotNone(StoreModel.find_by_name("Amazon store"))
                self.assertEqual(400, res.status_code)
                self.assertDictEqual(
                    {'message': "A store with name 'Amazon store' already exists."},
                    json.loads(res.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Oculus store")
                self.assertIsNotNone(StoreModel.find_by_name("Oculus store"))
                
                res = client.delete(
                    "/store/Oculus store")
                self.assertIsNone(StoreModel.find_by_name("Oculus store"))
                self.assertEqual(200, res.status_code)
                self.assertDictEqual(
                    {'message': 'Store deleted'},
                    json.loads(res.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Oculus store")
                self.assertIsNotNone(StoreModel.find_by_name("Oculus store"))
                
                res = client.get("/store/Oculus store")
                self.assertDictEqual(
                    {"name": "Oculus store","items": []}, 
                    json.loads(res.data))
                self.assertEqual(200, res.status_code)

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                res = client.get("/store/Unkown store")
                self.assertDictEqual(
                    {'message': 'Store not found'}, 
                    json.loads(res.data))
                self.assertEqual(404, res.status_code)

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Amazon store")
                ItemModel("item1", 1111, 1).save_to_db()
                ItemModel("item2", 2222, 1).save_to_db()

                res = client.get("/store/Amazon store")
                self.assertDictEqual(
                    {"name": "Amazon store",
                        "items": [
                            {"name": "item1", "price": 1111},
                            {"name": "item2", "price": 2222}
                        ]
                    }, 
                    json.loads(res.data))
                self.assertEqual(200, res.status_code)

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Amazon store")
                res = client.get("/stores")
                expected = {
                    "stores": [
                        {"name": "Amazon store","items": []}
                    ]
                }
                self.assertDictEqual(expected, json.loads(res.data))
                self.assertEqual(200, res.status_code)

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    "/store/Google store")
                ItemModel("item1", 1111, 1).save_to_db()
                ItemModel("item2", 2222, 1).save_to_db()
                client.post(
                    "/store/Amazon store")
                client.post(
                    "/store/Oculus store")
                
                res = client.get("/stores")
                expected = {
                    "stores":
                    [
                        {"name": "Google store",
                            "items": [
                                {"name": "item1", "price": 1111},
                                {"name": "item2", "price": 2222}
                            ]
                        },
                        {"name": "Amazon store", "items": []},
                        {"name": "Oculus store", "items": []},
                    ]
                }

                self.assertDictEqual(expected, json.loads(res.data))
                self.assertEqual(200, res.status_code)

