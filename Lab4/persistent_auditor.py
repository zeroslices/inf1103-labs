
def load_inventory():
    """
    Loads the inventory from a file.
    If the file does not exist, it initializes the inventory to 0.
    """
    try:
        with open("inventory.txt", "r") as file:
            print(file.read())
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_inventory(inventory):
    """
    Saves the current inventory to a file.
    """
    # with open("inventory.txt", "w") as file:
    #     file.write(str(inventory))

inventory = load_inventory()

def check_valid_input(userInput):
    """
    Checks if the user input is a valid integer or "quit".
    Returns True if valid, False otherwise.
    """

    try:
        quantity = int(userInput)
        if quantity < 0:
            print("Please enter a non-negative number.\n")
            return False
        return quantity
    except ValueError:
        print("Please enter a valid number.\n")
        return False

def get_valid_input(failedEntries, option = None):
    """
    Handles the prompt, handles input validation, and
    returns a valid integer or a "quit" signal.
    """
    question = "Quantity"
    if option == "item":
        question = "Product Name"
    userInput = input(f"Enter {question} or quit: ")

    if userInput.lower() == "quit":
        return userInput, failedEntries

    if option == None:
        userInput = check_valid_input(userInput)
        if userInput == False:
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

def main():

    failedEntries = 0
    transaction_history = []
    index = 1001

    while True:

        itemname, failedEntries = get_valid_input(failedEntries, "item")
        quantity, failedEntries = get_valid_input(failedEntries)

        
        if quantity == "quit" or itemname == "quit":
            generate_report(inventory, failedEntries)
            break

        
        
        transaction_history.append((index, itemname, quantity))
        
        print(f"Transaction History: {transaction_history}\n")

        for index, item, quantity in transaction_history:
            print(f"Transaction ID: {index}, Item: {item}, Quantity: {quantity}")
            index += 1


if __name__ == "__main__":
    main()