
# Backend Assessment

## Project Overview

This project is a backend service built with Flask for managing transactions, including a basic UI to interact with the APIs. The service allows creating, updating, retrieving, and calculating the sum of transactions linked by parent-child relationships. The UI provides a simple, user-friendly way to interact with the APIs.

## Features

- Create or update transactions with optional parent-child relationships.
- Retrieve transactions by ID or type.
- Calculate the sum of all transactions that are transitively linked by their parent ID.
- Simple UI for testing and interacting with the APIs.

### Prerequisites

- Python 3.x
- MySQL server (e.g., XAMPP or standalone MySQL)
- Git


UI Guide

  The UI is a simple interface that allows you to interact with the backend APIs directly from your browser.

    Access the UI: Go to http://127.0.0.1:5000/ in your web browser.

    Create or Update a Transaction: Enter the transaction details (ID, amount, type, and optional parent ID) and click Submit.

    Retrieve a Transaction by ID: Enter the Transaction ID and click Get Transaction.

    Retrieve Transactions by Type: Enter the type of transactions and click Get Transactions.
    
    Calculate Sum of Linked Transactions: Enter the Transaction ID and click Get Sum.


Asymptotic Behavior

  Time and Space Complexity

    Create or Update Transaction (PUT /transactionservice/transaction/<transaction_id>)
      Time Complexity: O(1) due to direct access or insertion.
      Space Complexity: O(1) per transaction.

    Retrieve a Transaction by ID (GET /transactionservice/transaction/<transaction_id>)
      Time Complexity: O(1) for direct retrieval using the primary key.
      Space Complexity: O(1) as it retrieves a single transaction.

    Retrieve Transactions by Type (GET /transactionservice/types/<type>)
      Time Complexity: O(n) where n is the number of matching transactions.
      Space Complexity: O(k) where k is the number of transactions returned.

    Iterative Sum Calculation for Linked Transactions
      Time Complexity: O(n) as each transaction is processed once.
      Space Complexity: O(h) where h is the depth of the hierarchy.

    Iterative Sum Calculation for Linked Transactions:

      Time Complexity: O(n), where n is the number of transactions.
      Space Complexity: O(h), where h is the depth of the hierarchy managed by the stack.

      Explanation: This method replaces recursion with an iterative approach using a manual stack, which helps prevent errors from too many nested calls (common in deep hierarchies). By managing the processing of transactions manually, it makes the system more reliable and capable of handling large and complex data structures without crashing.
