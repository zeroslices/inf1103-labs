inventory = 0
failedEntries = 0
while True:
    userInput = input("Enter a stock quantity or quit: ")

    if userInput == "quit":
        print("Total Units Processed: ", inventory)
        print("Total Failed Entries: ", failedEntries)
        break

    try:
        quantity = int(userInput)
    except ValueError:
        print("Please enter a valid number.")
        failedEntries += 1
        continue

    if quantity < 0:
        print("Please enter a non-negative number.")
        failedEntries += 1
        continue

    inventory += quantity
    print(inventory)
    if inventory > 500:
        print("Inventory limit exceeded.")
        break