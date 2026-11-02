from abc import ABC, abstractmethod
from can_be_shipped import CanBeShipped

@abstractmethod


class Product(ABC):
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

    @abstractmethod
    def get_fulfilment_info(self):
        """Abstract method to get fulfilment information for the product.
        This method should be implemented by subclasses."""
        pass

class PhysicalProduct(Product):
    """
    Represents a physical product in the inventory.
    Attributes:
        weight (float): The weight of the physical product in kilograms.
    """
    def __init__(self, product_id, name, price, stock, weight):
        """Initializes a PhysicalProduct instance with the given attributes."""
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        """Displays the physical product information in a formatted manner."""
        super().display_information()
        print(f"Weight: {self.__weight} kg\n")

    def get_fulfilment_info(self):
        """Returns the fulfilment information for the physical product."""
        return f"This is a physical product which requires physical shipping"

    def calculate_shipping_cost(self):
        """Calculates the shipping cost for the physical product based on its weight.
        Returns:
            float: The calculated shipping cost."""
        base_cost = 5.0  # Base shipping cost
        cost_per_kg = 2.0  # Cost per kilogram
        shipping_cost = base_cost + (cost_per_kg * self.__weight)
        return shipping_cost

class DigitalProduct(Product):
    """
    Represents a digital product in the inventory.
    Attributes:
        download_size (int): The size of the digital product in kilobytes (KB).
    """
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        """Displays the digital product information in a formatted manner."""
        super().display_information()
        print(f"Download Size: {self.__download_size} KB\n")

    def get_fulfilment_info(self):
        """Returns the fulfilment information for the digital product."""
        return f"This is a digital product which is delivered digitally"