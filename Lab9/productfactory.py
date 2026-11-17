
from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, 
               stock_quantity: int, supplier: Supplier | None = None, 
               weight: float | None= None, download_size: int | None =None) -> Product:
        if product_type == "physical":
            if weight is None:
                raise ValueError("Physical products need a weight")
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        elif product_type == "digital":
            if download_size is None:
                raise ValueError("Digital products need a download size")
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")