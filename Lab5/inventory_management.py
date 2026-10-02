import json
import os

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
            history = data["history"]
            print("inventory.json found.")
    except FileNotFoundError:
        print("inventory.json not found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print("Error decoding inventory.json. Starting with empty inventory.")
    print(history)
    print("Inventory loaded successfully." )
    return history

def save_inventory(history):
    """
    Saves the current inventory to a JSON file.
    """
    with open(INVENTORY_FILE, "w") as file:
        contents = {}
        contents["history"] = history
        # print(contents)
        json.dump(contents, file)
    print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}\n")

def validate_options(input):
    """
    Checks if the user input is a valid option.
    Returns True if it is, False otherwise.
    """
    return isinstance(input, str) and input in ["1", "2", "3", "4", "5", "6"]

def display_all_products(transaction_history):
    """
    Displays all products in the transaction history.
    """
    if not transaction_history:
        print("No products found.\n")
        return
    print(transaction_history)
    print("Current Inventory:")
    print("----------------------")
    for item in transaction_history:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: {item['price']} | Stock: {item['stock']}")
    print("----------------------\n")

def add_product(transaction_history):
    """
    Adds a new product to the transaction history.
    """
    print("\nAdd New Product")
    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    product_price = float(input("Price: "))
    product_stock = int(input("Stock Quantity: "))
    transaction_history.append({
        "id": product_id,
        "name": product_name,
        "price": f"{product_price:.2f}",
        "stock": product_stock
    })

    print(f"\nProduct added successfully!\n")
    return transaction_history

def update_stock(transaction_history):
    """
    Updates the stock quantity of an existing product.
    """
    product_id = input("\nEnter Product ID to update stock: ")
    for item in transaction_history:
        if item['id'] == product_id:
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}\n")
            new_stock = int(input(f"Enter new stock quantity for {item['name']}: "))
            item['stock'] = new_stock
            print(f"Stock updated successfully for {item['name']}.\n")
            return
    print("Product not found.\n")

def search_product(transaction_history):
    """
    Searches for a product by id in the transaction history.
    """
    product_id = input("\nEnter Product id to search: ")
    found_products = [item for item in transaction_history if item['id'] == product_id]
    
    if found_products:
        print("\nProduct(s) Found:")
        print("----------------------")
        for item in found_products:
            print(f"ID: {item['id']}\nName: {item['name']}\nPrice: {item['price']}\nStock: {item['stock']}")
        print("----------------------\n")
    else:
        print("\nProduct not found.\n")

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

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n\n")

    transaction_history = load_inventory()

    show_menu()
    while True:
        while True:
            choice = input("Enter option: ")
            if not validate_options(choice):
                print("Invalid option. Please try again.\n")
                show_menu()
                continue
            break

        match choice:
            case "1":
                display_all_products(transaction_history)
            case "2":
                add_product(transaction_history)
                # print(transaction_history)
            case "3":
                update_stock(transaction_history)
            case "4":
                search_product(transaction_history)
            case "5":
                print("\nSaving inventory...")
                save_inventory(transaction_history)

            case "6":
                print("\nSaving inventory before exit...")
                save_inventory(transaction_history)
                break
            case "_":
                print("Invalid option. Enter a valid option.\n")

    print("Thank you for using Inventory Management System.")
    print("Program terminated.")
        
if __name__ == "__main__":
    main()