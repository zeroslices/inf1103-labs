from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """
    Abstract base class representing the capability of a product to be shipped.
    Subclasses must implement the get_fulfilment_info method to provide specific fulfilment information.
    """
    
    @abstractmethod
    def calculate_shipping_cost(self):
        """Abstract method to calculate the shipping cost for the product.
        This method should be implemented by subclasses."""
        pass