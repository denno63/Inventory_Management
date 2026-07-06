import pytest
from app import app
import inventory
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        inventory.clear_all()
        yield client

def test_get_all_empty(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert response.json == []

def test_add_item(client):
    data = {'name': 'Test', 'price': 9.99, 'stock_quantity': 10, 'barcode': '123'}
    with patch('external_api.fetch_product_by_barcode') as mock_fetch:
        mock_fetch.return_value = {'product_name': 'Mock', 'brands': 'MB', 'ingredients_text': 'Mock'}
        response = client.post('/inventory', json=data)
        assert response.status_code == 201
        assert response.json['name'] == 'Test'
        assert response.json['product_name'] == 'Mock'

def test_get_one(client):
    with patch('external_api.fetch_product_by_barcode', return_value=None):
        post_resp = client.post('/inventory', json={'name': 'Item', 'price': 1, 'stock_quantity': 2})
    item_id = post_resp.json['id']
    response = client.get(f'/inventory/{item_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Item'

def test_get_one_not_found(client):
    response = client.get('/inventory/nonexistent')
    assert response.status_code == 404

def test_update_item(client):
    with patch('external_api.fetch_product_by_barcode', return_value=None):
        post_resp = client.post('/inventory', json={'name': 'Old', 'price': 1, 'stock_quantity': 5})
    item_id = post_resp.json['id']
    response = client.patch(f'/inventory/{item_id}', json={'price': 2.5})
    assert response.status_code == 200
    assert response.json['price'] == 2.5

def test_delete_item(client):
    with patch('external_api.fetch_product_by_barcode', return_value=None):
        post_resp = client.post('/inventory', json={'name': 'Del', 'price': 1, 'stock_quantity': 1})
    item_id = post_resp.json['id']
    response = client.delete(f'/inventory/{item_id}')
    assert response.status_code == 200
    get_resp = client.get(f'/inventory/{item_id}')
    assert get_resp.status_code == 404

def test_search_external(client):
    with patch('external_api.fetch_product_by_barcode') as mock_barcode, \
         patch('external_api.fetch_product_by_name') as mock_name:
        mock_barcode.return_value = {'product_name': 'BarcodeProd', 'brands': 'B'}
        mock_name.return_value = {'product_name': 'NameProd', 'brands': 'N'}
        resp = client.get('/external/search?barcode=123')
        assert resp.status_code == 200
        assert resp.json['product_name'] == 'BarcodeProd'
        resp = client.get('/external/search?name=apple')
        assert resp.status_code == 200
        assert resp.json['product_name'] == 'NameProd'
        resp = client.get('/external/search')
        assert resp.status_code == 400