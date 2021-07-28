from tests.unit.unite_base_test import UniteBaseTest
from models.store import StoreModel


class StoreTest(UniteBaseTest):
    def test_create_store(self):
        store = StoreModel("Test store")
        self.assertEqual(store.name, "Test store")
