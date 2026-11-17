from product import Product

class Inventory():
    """
    Manages a collection of products in the inventory.
    """
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def search_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("Current Inventory:")
        print("----------------------")
        if not self.__products:
            print("No products in inventory.\n")
            return
        for product in self.__products:
            product.display_information()

    def get_products(self):
        return list(self.__products)

    def remove_product(self, product_id: str):
        product = self.search_product(product_id)
        if product:
            self.__products.remove(product)
            print(f"Product with ID {product_id} removed from inventory.")
        else:
            print(f"No product found with ID {product_id}.")

    def show_product_details(self, product: Product) -> None:
        product.display_information()
        print(product.get_fulfilment_info())