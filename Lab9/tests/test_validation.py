"""Validation: each class rejects invalid data with a ValueError."""
import unittest

from orderline import OrderLine
from productfactory import ProductFactory


def make_lamp(price=25.0, stock=10):
    return ProductFactory.create("physical", "P001", "Lamp", price, stock, weight=1.0)


class TestProductValidation(unittest.TestCase):
    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            make_lamp(price=0)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            make_lamp(price=-5)

    def test_negative_stock_rejected(self):
        with self.assertRaises(ValueError):
            make_lamp(stock=-1)

    def test_zero_stock_allowed(self):
        self.assertEqual(make_lamp(stock=0).get_stock(), 0)

    def test_update_stock_negative_rejected(self):
        lamp = make_lamp()
        with self.assertRaises(ValueError):
            lamp.update_stock(-3)
        self.assertEqual(lamp.get_stock(), 10)   # unchanged

    def test_digital_negative_download_size_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 49.9, 100, download_size=-1)


class TestOrderLineValidation(unittest.TestCase):
    def test_zero_quantity_rejected(self):
        with self.assertRaises(ValueError):
            OrderLine(make_lamp(), 0)

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValueError):
            OrderLine(make_lamp(), -2)

    def test_valid_quantity_subtotal(self):
        self.assertEqual(OrderLine(make_lamp(), 4).calculate_subtotal(), 100)


if __name__ == "__main__":
    unittest.main()