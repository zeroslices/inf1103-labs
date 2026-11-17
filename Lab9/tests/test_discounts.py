import unittest

from discountstrategy import (DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount)

from order import Order
from productfactory import ProductFactory

def make_order(discount=None):
    chair = ProductFactory.create("physical", "P001", "Chair", 50.0, 10, weight=5.0)
    order = Order("O001", discount)
    order.add_order_line(chair, 5)
    return order

class TestStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_percentage_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_bulk_discount_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 230)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)

    def test_student_discount(self):
        self.assertAlmostEqual(StudentDiscount().apply(100), 250)

    class TestOrderUsesStrategy(unittest.TestCase):
        def test_default_is_no_discount(self):
            self.assertEqual(make_order().calculate_total(), 250)

        def test_order_delegates_to_strategy(self):
            class SpyDiscount(DiscountStrategy):
                def __init__(self):
                    self.received = None

                def apply(self, total):
                    self.received = total
                    return 1.0

            spy = SpyDiscount()
            self.assertEqual(make_order(spy).calculate_total, 1.0)
            self.assertEqual(spy.received, 250)

        def test_new_strategy_works_without_changing_order(self):
            self.assertAlmostEqual(make_order(StudentDiscount()).calculate_total(), 237.5)

        def test_set_discount_replaces_strategy(self):
            order = make_order(BulkDiscount(200, 20))
            self.assertEqual(order.calculate_total(), 230)
            order.set_discount(PercentageDiscount(10))
            self.assertAlmostEqual(order.calculate_total(), 225)

if __name__ == "__main__":
    unittest.main()