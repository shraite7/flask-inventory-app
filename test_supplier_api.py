import pytest
from app import app, db, Supplier

@pytest.fixture
def client():
    # Set up an in-memory database for clean testing isolated from your real database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

# --- POSITIVE TEST CASES ---

def test_create_supplier_success(client):
    payload = {"name": "Acme Corp", "contact_email": "vendor@acme.com", "phone": "555-1234"}
    response = client.post('/api/suppliers', json=payload)
    assert response.status_code == 201
    assert response.json['name'] == "Acme Corp"

def test_get_suppliers_list(client):
    response = client.get('/api/suppliers')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_supplier_success(client):
    # First manually seed a supplier
    with app.app_context():
        s = Supplier(name="Test Vendor", contact_email="test@test.com")
        db.session.add(s)
        db.session.commit()
        s_id = s.id

    response = client.get(f'/api/suppliers/{s_id}')
    assert response.status_code == 200
    assert response.json['name'] == "Test Vendor"

def test_update_supplier_success(client):
    with app.app_context():
        s = Supplier(name="Old Name", contact_email="old@test.com")
        db.session.add(s)
        db.session.commit()
        s_id = s.id

    payload = {"name": "New Name"}
    response = client.put(f'/api/suppliers/{s_id}', json=payload)
    assert response.status_code == 200
    assert response.json['name'] == "New Name"

def test_delete_supplier_success(client):
    with app.app_context():
        s = Supplier(name="To Delete", contact_email="delete@test.com")
        db.session.add(s)
        db.session.commit()
        s_id = s.id

    response = client.delete(f'/api/suppliers/{s_id}')
    assert response.status_code == 200

# --- NEGATIVE TEST CASES ---

def test_create_supplier_missing_fields(client):
    payload = {"phone": "12345"} # Missing name and email
    response = client.post('/api/suppliers', json=payload)
    assert response.status_code == 400

def test_get_supplier_not_found(client):
    response = client.get('/api/suppliers/999')
    assert response.status_code == 404

def test_update_supplier_not_found(client):
    response = client.put('/api/suppliers/999', json={"name": "No One"})
    assert response.status_code == 404

def test_delete_supplier_not_found(client):
    response = client.delete('/api/suppliers/999')
    assert response.status_code == 404