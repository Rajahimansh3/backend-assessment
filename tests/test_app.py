import pytest
from app import app
from db import get_db_connection

@pytest.fixture
def client():
    # Create a test client using Flask's built-in testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_transaction(client):
    response = client.put('/transactionservice/transaction/1', json={
        'amount': 1000,
        'type': 'cars',
        'parent_id': None
    })
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_get_transaction(client):
    response = client.get('/transactionservice/transaction/1')
    assert response.status_code == 200
    assert 'amount' in response.json

def test_calculate_sum(client):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (id, amount, type, parent_id) VALUES (12, 5000, 'typeA', NULL)")
    cur.execute("INSERT INTO transactions (id, amount, type, parent_id) VALUES (13, 2000, 'typeB', 12)")
    conn.commit()
    cur.close()
    conn.close()

    response = client.get('/transactionservice/sum/12')
    assert response.status_code == 200
    assert response.json['sum'] == 7000
