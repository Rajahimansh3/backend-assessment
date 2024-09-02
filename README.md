# Backend Assessment

## Project Overview

This project is a backend service built with Flask for managing transactions, including a basic UI to interact with the APIs. The service allows creating, updating, retrieving, and calculating the sum of transactions linked by parent-child relationships. The UI provides a simple, user-friendly way to interact with the APIs.


## Asymptotic Behavior

## Optimizations

- **Indexing**: The performance of `SELECT` operations can decrease as the table grows if appropriate indexes are not present on frequently queried fields (`id`, `parent_id`, `type`).  
  **Optimization**: we need to make indexes correctly set up on these columns.

- **Query Efficiency**: The optimized approach fetches all transactions in a single query and performs the sum calculation in memory, significantly reducing the number of database hits and improving performance over recursive approaches that involve multiple database queries.

- **Scalability**: The current approach scales well even with larger datasets due to its in-memory processing and iterative stack management, but for extremely large datasets, we can use optimizations such as caching or using database-level calculations (like:  SQL `WITH RECURSIVE`).

### Time and Space Complexity

1. **Create or Update Transaction (`PUT /transactionservice/transaction/<transaction_id>`)**
   - **Time Complexity**: `O(1)` due to direct access or insertion.
   - **Space Complexity**: `O(1)` per transaction.

2. **Retrieve a Transaction by ID (`GET /transactionservice/transaction/<transaction_id>`)**
   - **Time Complexity**: `O(1)` for direct retrieval using the primary key.
   - **Space Complexity**: `O(1)` as it retrieves a single transaction.

3. **Retrieve Transactions by Type (`GET /transactionservice/types/<type>`)**
   - **Time Complexity**: `O(n)` where `n` is the number of matching transactions.
   - **Space Complexity**: `O(k)` where `k` is the number of transactions returned.

4. **Iterative Sum Calculation for Linked Transactions**
    - **Time Complexity**: `O(n)`, where `n` is the number of transactions.
    - **Space Complexity**: `O(h)`, where `h` is the depth of the hierarchy managed by the stack.

    **Explanation**: This method replaces recursion with an iterative approach using a manual stack, which helps prevent errors from too many nested calls (common in deep hierarchies). By managing the processing of transactions manually, it makes the system more reliable and capable of handling large and complex data structures without crashing.


## UI Guide for APIs testing

The UI is a simple interface that allows you to interact with the backend APIs directly from your browser.

- **Access the UI**: Go to `http://127.0.0.1:5000/` in your web browser.
- **Create or Update a Transaction**: Enter the transaction details (ID, amount, type, and optional parent ID) and click **Submit**.
- **Retrieve a Transaction by ID**: Enter the Transaction ID and click **Get Transaction**.
- **Retrieve Transactions by Type**: Enter the type of transactions and click **Get Transactions**.
- **Calculate Sum of Linked Transactions**: Enter the Transaction ID and click **Get Sum**.

## Testing using pytest

This project uses `pytest` for unit testing. The tests cover:
- API endpoint validation.
- Correctness of transaction creation, retrieval, and sum calculations.

### Running Tests

To run the tests, ensure you are in the project directory and use the following command:

```bash
PYTHONPATH=./ pytest tests/


## Features

- Create or update transactions with optional parent-child relationships.
- Retrieve transactions by ID or type.
- Calculate the sum of all transactions that are transitively linked by their parent ID.
- Simple UI for testing and interacting with the APIs.

### Prerequisites

- Python 3.x
- MySQL server (e.g., XAMPP or standalone MySQL)
- Git