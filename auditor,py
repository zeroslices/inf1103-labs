inventory = 0
failedEntries = 0
while True:
    userInput = input("Enter a stock quantity or quit: ")

    if userInput == "quit":
        print("Total Units Processed: ", inventory)
        print("Total Failed Entries: ", failedEntries)
        break

    if not userInput.isdigit():
        print("Please enter a valid number.")
        failedEntries += 1
        continue

    inventory += int(userInput)
    print(inventory)
    if inventory > 500:
        print("Inventory limit exceeded.")
        break