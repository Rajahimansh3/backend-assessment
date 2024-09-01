from flask import Flask,render_template, request, jsonify
from db import get_db_connection
from config import Config 

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration

# Endpoint to create or update a transaction
@app.route('/transactionservice/transaction/<int:transaction_id>', methods=['PUT'])
def add_transaction(transaction_id):

    if transaction_id is None or str(transaction_id).strip() == '' or transaction_id < 0:
        return jsonify({"error": "Transaction ID must not be empty, blank, or negative"}), 400

    data = request.json
    amount = data.get('amount')
    type = data.get('type')
    parent_id = data.get('parent_id', None)

    # Error handling
    if not amount or not type :
        return jsonify({"error": "Amount and type are required fields and cannot be empty."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cur = conn.cursor()

    try:
        if parent_id is not None: # Check if parent_id exists
            cur.execute("SELECT id FROM transactions WHERE id = %s", (parent_id,))
            parent_exists = cur.fetchone()
            if not parent_exists:
                return jsonify({"error": f"Parent ID {parent_id} does not exist."}), 400

        # Insert or update the transaction
        cur.execute("""
            INSERT INTO transactions (id, amount, type, parent_id)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE amount=%s, type=%s, parent_id=%s;
        """, (transaction_id, amount, type, parent_id, amount, type, parent_id))
        conn.commit()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 400
    finally:
        cur.close()
        conn.close()


# Endpoint to get a transaction by ID
@app.route('/transactionservice/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):

    if transaction_id is None or str(transaction_id).strip() == '' or transaction_id < 0:
        return jsonify({"error": "Transaction ID must not be empty, blank, or negative"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT amount, type, parent_id FROM transactions WHERE id = %s", (transaction_id,))
        row = cur.fetchone()
        if row:
            return jsonify({"amount": row[0], "type": row[1], "parent_id": row[2]}), 200
        else:
            return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 400
    finally:
        cur.close()
        conn.close()

# Endpoint to get all transactions by type
@app.route('/transactionservice/types/<string:type>', methods=['GET'])
def get_transactions_by_type(type):

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM transactions WHERE type = %s", (type,))
        rows = cur.fetchall()
        return jsonify([row[0] for row in rows]), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 400
    finally:
        cur.close()
        conn.close()

# Recursive function to calculate the sum of all linked transactions
def calculate_sum(transaction_id):
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return None  

    cur = conn.cursor()
    try:
        # Fetch the base amount of the current transaction
        cur.execute("SELECT amount FROM transactions WHERE id = %s", (transaction_id,))
        base_amount = cur.fetchone()
        
        if not base_amount:
            print(f"Transaction ID {transaction_id} not found.")
            return None 

        base_amount = base_amount[0] 

        # Fetch all child transactions linked by parent_id
        cur.execute("SELECT id FROM transactions WHERE parent_id = %s", (transaction_id,))
        children = cur.fetchall()        

        if children is None:
            children = []

    except Exception as e:
        print(f"Unexpected error during sum calculation: {str(e)}")
        return None
    finally:
        cur.close()
        conn.close()

    # Calculate the total sum including all linked child transactions
    total = base_amount
    for child in children:
        child_id = child[0]
        child_sum = calculate_sum(child_id)
        if child_sum is None:
            print(f"Error calculating sum for child transaction ID {child_id}.")
            return None

        total += child_sum

    return total

# Endpoint to get the sum of all linked transactions
@app.route('/transactionservice/sum/<int:transaction_id>', methods=['GET'])
def get_transaction_sum(transaction_id):

    if transaction_id is None or str(transaction_id).strip() == '' or transaction_id < 0:
        return jsonify({"error": "Transaction ID must not be empty, blank, or negative"}), 400
    
    try:
        total_sum = calculate_sum(transaction_id)
        
        if total_sum is None: # Check for errors
            return jsonify({"error": f"Unable to calculate sum for transaction ID {transaction_id} due to missing data or connection failure."}), 400
        return jsonify({"sum": total_sum}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Basic route for testing server
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

