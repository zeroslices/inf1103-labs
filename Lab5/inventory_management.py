import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", BASE_DIR)   # Docker sets this to /data
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

def load_inventory():
    """Returns (total, history). Starts empty if the file is missing."""
    history = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
            history = data["history"]
            print("inventory.json found.")
    except FileNotFoundError:
        return history
    print(history)
    print("Inventory loaded successfully." )
    return history

def save_inventory(history):
    """
    Saves the total and transaction history to inventory.json.
    Format: first line is the total, then one 'id,item,qty' line per order.
    """
    with open(INVENTORY_FILE, "w") as file:
        contents = {}
        contents["history"] = history
        # print(contents)
        json.dump(contents, file)
    print(f"Order successfully saved to {os.path.basename(INVENTORY_FILE)}")

def check_valid_input(userInput):
    """
    Checks if the user input is a valid integer or "quit".
    Returns True if valid, False otherwise.
    """

    try:
        quantity = int(userInput)
        if quantity < 0:
            print("Please enter a non-negative number.\n")
            return None
        return quantity
    except ValueError:
        print("Please enter a valid number.\n")
        return None

def get_valid_input(failedEntries, option = None):
    """
    Handles the prompt, handles input validation, and
    returns a valid integer or a "quit" signal.
    """
    question = "Quantity"
    if option == "item":
        question = "Product Name"
    userInput = input(f"Enter {question} or quit: ")

    if check_quit(userInput):
        return userInput, failedEntries

    if option == None:
        userInput = check_valid_input(userInput)
        if userInput == None:
            failedEntries += 1
            return get_valid_input(failedEntries)
    
    
    return userInput, failedEntries

def process_delivery(current_total, new_value): 
    """
    Calculates the new total and
    returns it.
    """
    return current_total + new_value
    
def calculate_tax(amount):
    """
    A new requirement! This function takes a delivery
    amount and returns the tax (10% of that specific delivery).
    """
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    """
    A dedicated function to print
    the final summary.
    """
    print("Final Report:")
    print("Total Units Processed: ", total_units)
    print("Total Failed Entries: ", failed_attempts)
    return

def check_quit(userInput):
    """
    Checks if the user input is "quit".
    Returns True if it is, False otherwise.
    """
    return isinstance(userInput, str) and userInput.lower() == "quit"

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
        print("Product not found.\n")

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
                pass    
            case "6":
                save_inventory(transaction_history)
                break
            case "_":
                print("Invalid option. Enter a valid option.\n")

    print("Thank you for using Inventory Management System.")
    print("Program terminated.")

    # print(total, transaction_history)
    failedEntries = 0

    # while True:
    #     print(f"Total Units: {total}", f"Transaction History: {transaction_history}\n")
    #     itemname, failedEntries = get_valid_input(failedEntries, "item")

    #     if check_quit(itemname):
    #         generate_report(total, failedEntries)
    #         save_inventory(total, transaction_history)
    #         break

    #     quantity, failedEntries = get_valid_input(failedEntries)

    #     if check_quit(quantity):
    #         generate_report(total, failedEntries)
    #         save_inventory(total, transaction_history)
    #         break

    #     print(f"New Order Added:\nIndex: {index}, Item: {itemname}, Quantity: {quantity}\n")

    #     total = process_delivery(total, quantity)

    #     transaction_history.append((index, itemname, quantity))

    #     index += 1
        
    #     # print(f"Transaction History: {transaction_history}\n")

    #     for tid, item, qty in transaction_history:
    #         print(f"Transaction ID: {tid}, Item: {item}, Quantity: {qty}")

        

if __name__ == "__main__":
    main()