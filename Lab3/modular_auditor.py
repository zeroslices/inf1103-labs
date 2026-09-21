inventory = 0
failedEntries = 0

def get_valid_input(failedEntries):
    """
    Handles the prompt, handles input validation, and
    returns a valid integer or a "quit" signal.
    """
    userInput = input("Enter a stock quantity or quit: ")

    if userInput == "quit":
        return userInput, failedEntries

    try:
        quantity = int(userInput)
    except ValueError:
        print("Please enter a valid number.\n")
        failedEntries += 1
        return get_valid_input(failedEntries)

    if quantity < 0:
        print("Please enter a non-negative number.\n")
        failedEntries += 1
        return get_valid_input(failedEntries)
            
    return quantity, failedEntries

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
    print("Total Units Processed: ", total_units)
    print("Total Failed Entries: ", failed_attempts)
    return

while True:
    # userInput = input("Enter a stock quantity or quit: ")

    # if userInput == "quit":
    #     print("Total Units Processed: ", inventory)
    #     print("Total Failed Entries: ", failedEntries)
    #     break

    # try:
    #     quantity = int(userInput)
    # except ValueError:
    #     print("Please enter a valid number.")
    #     failedEntries += 1
    #     continue

    quantity, failedEntries = get_valid_input(failedEntries)

    if quantity == "quit":
        generate_report(inventory, failedEntries)
        break

    # if quantity < 0:
    #     print("Please enter a non-negative number.")
    #     failedEntries += 1
    #     continue

    inventory = process_delivery(inventory, quantity)
    print("Current Inventory:",inventory, "\n")
    if inventory > 500:
        print("Inventory limit exceeded.")
        break