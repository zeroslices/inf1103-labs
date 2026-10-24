class Product:
    """
    Manages a product in the inventory.
    Attributes:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
        stock_quantity (int): The quantity of the product in stock.
    """
    def __init__(self, product_id, name, price, stock_quantity):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock_quantity = stock_quantity

    def update_stock(self, new_stock):
        self.__stock_quantity = new_stock

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: {self.__price:.2f} | Stock: {self.__stock_quantity}")