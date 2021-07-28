from tests.base_test import BaseTest

from models.store import StoreModel
from models.item import ItemModel


class StoreTest(BaseTest):
    def test_save_store(self):
        with self.app_context():
            store = StoreModel("Amazon")
            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("Amazon"))

    def test_delete_store(self):
        with self.app_context():
            store = StoreModel("Amazon")
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("Amazon"))

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name("Amazon"))

    def test_relationship(self):
            with self.app_context():
                store = StoreModel("Google store")
                item = ItemModel("Greate product", 99.99, 1)

                store.save_to_db()
                item.save_to_db()
                self.assertEqual(store.items.count(), 1)
                self.assertEqual(store.items.first().name, "Greate product")

    def test_json_no_item(self):
        with self.app_context():
            store = StoreModel("Store 1")
            store_json = store.json()
            expected_json = {
                "name": "Store 1",
                "items": []
            }

            self.assertDictEqual(expected_json, store_json)

    def test_json_with_single_item(self):
        with self.app_context():
            store = StoreModel("Store 2")
            item1 = ItemModel("Item1", 12.0, 1)

            store.save_to_db()
            item1.save_to_db()
            store_json = store.json()
            expected_json = {
                "name": "Store 2",
                "items": [{"name": "Item1", "price": 12.0}]
            }

            self.assertDictEqual(expected_json, store_json)

    def test_json_with_multiple_item(self):
        with self.app_context():
            store = StoreModel("Store 3")
            item1 = ItemModel("Item1", 12.0, 1)
            item2 = ItemModel("Item2", 24.0, 1)

            store.save_to_db()
            item1.save_to_db()
            item2.save_to_db()
            store_json = store.json()
            expected_json = {
                "name": "Store 3",
                "items": [
                    {"name": "Item1", "price": 12.0},
                    {"name": "Item2", "price": 24.0},
                    ]
            }

            self.assertDictEqual(expected_json, store_json)