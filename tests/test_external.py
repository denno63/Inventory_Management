from unittest.mock import patch
import external_api

def test_fetch_by_barcode_success():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 1,
            'product': {'product_name': 'Milk', 'brands': 'Dairy', 'ingredients_text': 'Milk'}
        }
        result = external_api.fetch_product_by_barcode('123')
        assert result['product_name'] == 'Milk'

def test_fetch_by_barcode_not_found():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 0}
        result = external_api.fetch_product_by_barcode('999')
        assert result is None

def test_fetch_by_name_success():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'products': [{'product_name': 'Banana', 'brands': 'Chiquita', 'ingredients_text': 'Banana'}]
        }
        result = external_api.fetch_product_by_name('banana')
        assert result['product_name'] == 'Banana'