class Product:
    """
    Manages a product in the inventory.
    Attributes:
        product_id (str): The unique identifier for the product.
        name (str): The name of the product.
        price (float): The price of the product.
        stock (int): The quantity of the product in stock.
    """
    def __init__(self, product_id, name, price, stock):
        """Initializes a Product instance with the given attributes."""
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, new_stock):
        """Updates the stock quantity of the product.
        Args:
            new_stock (int): The new stock quantity to set."""
        
        if not isinstance(new_stock, int) or new_stock < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")
        self.__stock = new_stock
        print("Stock updated successfully. New stock quantity:", self.__stock)

    def get_product_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__name
    
    def get_price(self): 
        return self.__price

    def get_stock(self):
        return self.__stock

    def display_information(self):
        """Displays the product information in a formatted manner."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}\n")