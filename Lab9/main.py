import json
import os

from productfactory import ProductFactory
from supplier import Supplier
from product import PhysicalProduct, DigitalProduct
from inventory import Inventory
from order import Order
from helper import get_positive_float

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)   # Docker sets this to /data
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path)
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Products file is not valid JSON: {e}")
                return
        records = data.get("history", []) if isinstance(data, dict) else [] 
        loaded = 0
        for i, record in enumerate(records, start=1):
            try:
                if inventory.search_product(record["id"]):
                    raise ValueError(f"duplicate product ID {record["id"]}")
                product = ProductFactory.create(
                    record["product_type"], record["id"], record["name"],
                           float(record["price"]), int(record["stock"]), supplier,
                           weight = record.get("weight"), download_size = record.get("download_size"),
                )
            except (ValueError, KeyError, TypeError) as e:
                print(f"Skipping product #{i}: {e!r}")
                continue
            inventory.add_product(product)
            loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

# def load_inventory():
#     """
#     Loads the inventory from a JSON file.
#     If the file does not exist, it initializes an empty inventory."""
#     history = []
#     try:
#         with open(INVENTORY_FILE, "r") as file:
#             data = json.load(file)
#             history = data.get("history", [])
#             print("inventory.json found.")
#     except FileNotFoundError:
#         print("inventory.json not found. Starting with empty inventory.")
#     except json.JSONDecodeError:
#         print("Error decoding inventory.json. Starting with empty inventory.")
#     # print(history)
#     print("Inventory loaded successfully." )
#     return history

def save_inventory(inventory):
    """
    Saves the current inventory to a JSON file.
    """
    history = [
        {"id": product.get_product_id(), "name": product.get_name(),
        "price": product.get_price(), "stock": product.get_stock(), "product_type": "physical" if isinstance(product, PhysicalProduct) else "digital", 
        "weight": product.get_weight() if isinstance(product, PhysicalProduct) else None,
        "download_size": product.get_download_size() if isinstance(product, DigitalProduct) else None} 
        for product in inventory.get_products()
        ]
    content = json.dumps({"history": history}, indent=4)
    with open(INVENTORY_FILE, "w") as file:
        file.write(content)
    print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}\n")

def validate_options(input):
    """
    Checks if the user input is a valid option.
    Returns True if it is, False otherwise.
    """
    return isinstance(input, str) and input in ["1", "2", "3", "4", "5", "6"]

# def build_inventory(history):
#     """
#     Builds the inventory from the transaction history.
#     """
#     inventory = Inventory()
#     for product_data in history:
#         product_type = "physical" if product_data.get("weight") is not None else "digital"
#         product = ProductFactory.create(product_type, product_data["id"], product_data["name"],
#                                         product_data["price"], product_data["stock"],
#                                         weight = product_data.get("weight"),
#                                         download_size= product_data.get("download_size"))
#         inventory.add_product(product)
#     return inventory

def show_menu():
    """
    Displays the menu options to the user.
    """
    print("----------- MENU ----------- ")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------\n")

def new_product_details():
    """
    Prompts the user for product details and returns them as a dictionary.
    """
    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    price = get_positive_float("Enter Product Price: ")
    stock = int(input("Enter Product Stock Quantity: "))
    product_type = input("Enter Product Type (physical/digital): ").strip().lower()
    details = {"type": product_type, "id": product_id, "name": name, "price": price, "stock": stock}
    if product_type == "physical":
        details["weight"] = get_positive_float("Enter Product Weight (kg): ")
    
    elif product_type == "digital":
        details["download_size"] = int(input("Enter Product Download Size (KB): "))
    # return {"id": product_id, "name": name, "price": price, "stock": stock}
    return details

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n\n")
    
    inventory = Inventory()
    load_products(DATA_DIR, inventory, supplier=None)

    while True:

        show_menu()

        while True:
            choice = input("Enter option: ")
            if not validate_options(choice):
                print("Invalid option. Please try again.\n")
                continue
            break

        match choice:
            case "1":
                inventory.display_all()

            case "2":
                try:
                    product_info = new_product_details()
                except ValueError:
                    print("Invalid input. Please enter valid product details.\n")
                    continue
                if inventory.search_product(product_info["id"]):
                    print("Product with this ID already exists. Cannot add duplicate product.\n")
                    continue
                try:
                    product = ProductFactory.create(product_info["type"], product_info["id"],
                                                    product_info["name"], product_info["price"],
                                                    product_info["stock"],
                                                    weight = product_info.get("weight"),
                                                    download_size= product_info.get("download_size"))
                except ValueError as e:
                    print(f"Could not create product: {e}\n")
                    continue
                inventory.add_product(product)    
                inventory.display_all()    

            case "3":
                product_id = input("Enter Product ID to update stock: ")
                product = inventory.search_product(product_id)
                if product:
                    print("Product found. \nCurrent stock:", product.get_stock())
                    try:
                        new_stock = int(input("Enter new stock quantity: "))
                        product.update_stock(new_stock)
                    except ValueError as e:
                        print("Invalid Stock:", e)
                else:
                    print("Product not found.")

            case "4":
                product_id = input("Enter Product ID to search: ")
                product = inventory.search_product(product_id)
                if product:
                    print("Product found:")
                    product.display_information()
                else:
                    print("Product not found.")

            case "5":
                print("\nSaving inventory...")
                save_inventory(inventory)

            case "6":
                print("\nSaving inventory before exit...")
                save_inventory(inventory)
                break

            case _:
                print("Invalid option. Enter a valid option.\n")

    print("Thank you for using Inventory Management System.")
    print("Program terminated.")
        
if __name__ == "__main__":
    # print(digital_product.calculate_shipping_cost())
    main()
    # supplier = Supplier("S001", "ABC Supplies", "supplier@gmail.com")
    # digital_product = DigitalProduct("D001", "E-book", 19.99, 100, 2, supplier)
    # physical_product = PhysicalProduct("P001", "Laptop", 999.99, 50, 2.5, supplier)
    # del supplier
    # digital_product.supplier.display_information()
    # digital_product.display_information()

    # inventory_A = Inventory()
    # inventory_A.add_product(digital_product)
    # inventory_A.remove_product("D001")
    # inventory_B = Inventory()
    # inventory_B.add_product(digital_product)
    # inventory_B.add_product(physical_product)

    # order1 = Order("O001")
    # order1.add_order_line(digital_product, 2)
    # order1.add_order_line(physical_product, 3)

    # order2 = Order("O002")
    # order2.add_order_line(digital_product, 2)
    # order2.add_order_line(physical_product, 3)

    # print(order1.calculate_total())

    # inventory_B.show_product_details(digital_product)
    # inventory_B.show_product_details(physical_product)