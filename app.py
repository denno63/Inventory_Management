from flask import Flask, request, jsonify
import inventory
import external_api

app = Flask(__name__)

def validate_item_data(data):
    required = ['name', 'price', 'stock_quantity']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, ""

@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(inventory.get_all()), 200

@app.route('/inventory/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = inventory.get_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    valid, msg = validate_item_data(data)
    if not valid:
        return jsonify({'error': msg}), 400

    barcode = data.get('barcode')
    if barcode:
        external_info = external_api.fetch_product_by_barcode(barcode)
        if external_info:
            for key, value in external_info.items():
                if key not in data:
                    data[key] = value

    try:
        new_item = inventory.add_item(data)
        return jsonify(new_item), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/inventory/<string:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    updated = inventory.update_item(item_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'error': 'Item not found'}), 404

@app.route('/inventory/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    removed = inventory.delete_item(item_id)
    if removed:
        return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'error': 'Item not found'}), 404

@app.route('/external/search', methods=['GET'])
def search_external():
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    if barcode:
        result = external_api.fetch_product_by_barcode(barcode)
    elif name:
        result = external_api.fetch_product_by_name(name)
    else:
        return jsonify({'error': 'Provide either barcode or name parameter'}), 400
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)