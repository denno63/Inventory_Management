import requests

OPENFOODFACTS_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"

def fetch_product_by_barcode(barcode):
    url = OPENFOODFACTS_URL.format(barcode)
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 1 and 'product' in data:
            product = data['product']
            return {
                'product_name': product.get('product_name', ''),
                'brands': product.get('brands', ''),
                'ingredients_text': product.get('ingredients_text', ''),
            }
        return None
    except requests.exceptions.RequestException:
        return None

def fetch_product_by_name(name):
    search_url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        'search_terms': name,
        'json': 1,
        'page_size': 1
    }
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
        if products:
            product = products[0]
            return {
                'product_name': product.get('product_name', ''),
                'brands': product.get('brands', ''),
                'ingredients_text': product.get('ingredients_text', ''),
            }
        return None
    except requests.exceptions.RequestException:
        return None