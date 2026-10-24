import json
import os

from product import Product
from inventory import Inventory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)   # Docker sets this to /data
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")



def load_inventory():
    """
    Loads the inventory from a JSON file.
    If the file does not exist, it initializes an empty inventory."""
    history = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
            history = data.get("history", [])
            print("inventory.json found.")
    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print("Error decoding inventory.json. Starting with empty inventory.")
    # print(history)
    print("Inventory loaded successfully." )
    return history

def save_inventory(inventory):
    """
    Saves the current inventory to a JSON file.
    """
    history = [
        {"id": product.get_product_id(), "name": product.get_name(),
        "price": product.get_price(), "stock": product.get_stock()} 
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

def build_inventory(history):
    """
    Builds the inventory from the transaction history.
    """
    inventory = Inventory()
    for product_data in history:
        product = Product(product_data["id"], product_data["name"], product_data["price"], product_data["stock"])
        inventory.add_product(product)
    return inventory

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
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock Quantity: "))
    return {"id": product_id, "name": name, "price": price, "stock": stock}

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n\n")
    
    inventory = build_inventory(load_inventory())

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
                product = Product(product_info["id"], product_info["name"], product_info["price"], product_info["stock"])
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
    main()