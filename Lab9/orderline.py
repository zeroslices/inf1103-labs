from product import Product
class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity


    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity