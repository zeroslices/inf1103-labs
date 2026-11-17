
import unittest

from product import Product, PhysicalProduct, DigitalProduct
from productfactory import ProductFactory


class TestProductFactory(unittest.TestCase):
    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 1.5)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, download_size=500)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_download_size(), 500)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5)
        self.assertIn("Unknown product type: service", str(ctx.exception))

    def test_physical_without_weight_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 25.0, 10)

    def test_digital_without_download_size_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 49.9, 100)


if __name__ == "__main__":
    unittest.main()