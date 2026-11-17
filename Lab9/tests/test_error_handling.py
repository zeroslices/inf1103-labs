import io
import json
import os 
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from helper import get_positive_float
from inventory import Inventory
from main import load_products

class TestGetPositive(unittest.TestCase):
    def test_keeps_asking_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
            redirect_stdout(io.StringIO()) as out:
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertIn("Please enter a valid number", out.getvalue())
        self.assertIn("greater than zero", out.getvalue())


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "inventory.json")

    def tearDown(self):
        self.tmp.cleanup()

    def load(self, inventory):
        with redirect_stdout(io.StringIO()) as out:
            load_products(self.path, inventory, None)
        return out.getvalue()

    def test_missing_file_handled(self):
        inventory = Inventory()
        output = self.load(inventory)
        self.assertIn("not found", output)
        self.assertIn("Load attempt finished.", output)
        self.assertEqual(inventory.get_products(), [])

    def test_invalid_json_handled(self):
        with open(self.path, "w") as f:
            f.write("{not valid json")
        output = self.load(Inventory())
        self.assertIn("not valid JSON", output)
        self.assertIn("Load attempt finished.", output)

    def test_bad_records_skipped_good_records_load(self):
        records = [
            {"id": "P001", "name": "Desk Lamp", "price": 25.0, "stock": 10,
             "product_type": "physical", "weight": 1.0, "download_size": None},
            {"id": "D001", "name": "Photo Editor", "price": 49.9, "stock": 100,
             "product_type": "digital", "weight": None, "download_size": 500},
            {"id": "S001", "name": "Installation", "price": 30.0, "stock": 5,
             "product_type": "service"},
            {"id": "P002", "name": "Office Chair", "price": "abc", "stock": 3,
             "product_type": "physical", "weight": 2.0},
            {"id": "P003", "name": "Monitor Stand", "stock": 7,
             "product_type": "physical", "weight": 1.0},
        ]
        with open(self.path, "w") as f:
            json.dump({"history": records}, f)

        inventory = Inventory()
        output = self.load(inventory)

        ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001"])
        self.assertEqual(output.count("Skipping"), 3)
        self.assertIn("2 products loaded.", output)
        self.assertIn("Load attempt finished.", output)


if __name__ == "__main__":
    unittest.main()