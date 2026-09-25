# Inventory Auditor

A simple interactive Python program for processing stock quantities. It tracks the total inventory and the number of invalid entries submitted by the user.

## Features

- Accepts stock quantities as whole numbers.
- Rejects invalid input and counts failed entries.
- Displays the running inventory total.
- Stops when the user enters `quit`.
- Stops automatically when inventory exceeds 500 units.
- Includes a Docker configuration for containerized execution.

## Requirements

- Python 3.11 or later for local execution, or
- Docker for containerized execution.

## Run Locally

From this directory, run:

```bash
python auditor.py
```

Enter a whole-number stock quantity when prompted. Enter `quit` to finish and display the totals.

## Run with Docker

Build the image:

```bash
docker build -f dockerfile -t inventory-auditor .
```

Run the container interactively:

```bash
docker run -it --rm inventory-auditor
```

The `-it` option is required so the program can receive input from the terminal.

## Example

```text
Enter a stock quantity or quit: 100
100
Enter a stock quantity or quit: 25
125
Enter a stock quantity or quit: abc
Please enter a valid number.
Enter a stock quantity or quit: quit
Total Units Processed:  125
Total Failed Entries:  1
```

## Files

- `auditor.py` - Interactive inventory auditing program.
- `dockerfile` - Docker image configuration using Python 3.11 slim.
