
// Function to create or update a transaction
function createTransaction() {

    const transactionId = document.getElementById('transaction_id').value;
    const amount = document.getElementById('amount').value;
    const type = document.getElementById('type').value;
    const parentId = document.getElementById('parent_id').value || null;

    const data = {
        amount: parseFloat(amount),
        type: type,
        parent_id: parentId ? parseInt(parentId) : null
    };
    console.log("data",data);

    fetch(`/transactionservice/transaction/${transactionId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    
    .then(response => response.json())

    .then(data => {
        document.getElementById('results').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('results').textContent = 'Error: ' + error;
    });
}

// Function to get a transaction by ID
function getTransaction() {
    const transactionId = document.getElementById('get_transaction_id').value;

    fetch(`/transactionservice/transaction/${transactionId}`)

        .then(response => response.json())

        .then(data => {
            document.getElementById('results').textContent = JSON.stringify(data, null, 2);
        })

        .catch(error => {
            document.getElementById('results').textContent = 'Error: ' + error;
        });
}

// Function to get transactions using type
function getTransactionsByType() {
    const type = document.getElementById('get_type').value;

    fetch(`/transactionservice/types/${type}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = JSON.stringify(data, null, 2);
        })

        .catch(error => {
            document.getElementById('results').textContent = 'Error: ' + error;
        });
}

// Function to get the sum 
function getTransactionSum() {
    const transactionId = document.getElementById('sum_transaction_id').value;

    fetch(`/transactionservice/sum/${transactionId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('results').textContent = 'Error: ' + error;
        });
}
