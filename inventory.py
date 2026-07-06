import uuid

_inventory = []

def _generate_id():
    return str(uuid.uuid4())[:8]

def get_all():
    return _inventory

def get_by_id(item_id):
    for item in _inventory:
        if item['id'] == item_id:
            return item
    return None

def add_item(data):
    required = ['name', 'price', 'stock_quantity']
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    new_item = {'id': _generate_id()}
    new_item.update(data)
    _inventory.append(new_item)
    return new_item

def update_item(item_id, updates):
    item = get_by_id(item_id)
    if item is None:
        return None
    for key, value in updates.items():
        if key != 'id':
            item[key] = value
    return item

def delete_item(item_id):
    global _inventory
    item = get_by_id(item_id)
    if item is None:
        return False
    _inventory = [i for i in _inventory if i['id'] != item_id]
    return True

def clear_all():
    global _inventory
    _inventory = []