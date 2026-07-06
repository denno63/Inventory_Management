import requests
import sys

BASE_URL = "http://localhost:5000"

def print_item(item):
    print(f"ID: {item.get('id')}")
    print(f"Name: {item.get('name')}")
    print(f"Price: {item.get('price')}")
    print(f"Stock: {item.get('stock_quantity')}")
    print(f"Barcode: {item.get('barcode', 'N/A')}")
    print(f"Product Name (external): {item.get('product_name', 'N/A')}")
    print(f"Brands: {item.get('brands', 'N/A')}")
    print("-" * 30)

def view_all():
    resp = requests.get(f"{BASE_URL}/inventory")
    if resp.status_code == 200:
        items = resp.json()
        if not items:
            print("Inventory is empty.")
        else:
            for item in items:
                print_item(item)
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def view_one(item_id):
    resp = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if resp.status_code == 200:
        print_item(resp.json())
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def add_item():
    name = input("Product name: ")
    try:
        price = float(input("Price: "))
        stock = int(input("Stock quantity: "))
    except ValueError:
        print("Invalid number. Please try again.")
        return
    barcode = input("Barcode (optional, press Enter to skip): ").strip() or None

    data = {"name": name, "price": price, "stock_quantity": stock}
    if barcode:
        data["barcode"] = barcode

    resp = requests.post(f"{BASE_URL}/inventory", json=data)
    if resp.status_code == 201:
        print("Item added successfully:")
        print_item(resp.json())
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def update_item():
    item_id = input("Enter item ID to update: ")
    print("Enter fields to update (leave blank to skip):")
    name = input("New name: ").strip()
    price_str = input("New price: ").strip()
    stock_str = input("New stock quantity: ").strip()
    barcode = input("New barcode: ").strip()

    updates = {}
    if name:
        updates['name'] = name
    if price_str:
        try:
            updates['price'] = float(price_str)
        except ValueError:
            print("Invalid price, skipping.")
    if stock_str:
        try:
            updates['stock_quantity'] = int(stock_str)
        except ValueError:
            print("Invalid stock, skipping.")
    if barcode:
        updates['barcode'] = barcode

    if not updates:
        print("No fields to update.")
        return

    resp = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=updates)
    if resp.status_code == 200:
        print("Item updated:")
        print_item(resp.json())
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def delete_item():
    item_id = input("Enter item ID to delete: ")
    resp = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if resp.status_code == 200:
        print("Item deleted successfully.")
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def search_external():
    choice = input("Search by (b)arcode or (n)ame? ").lower()
    if choice == 'b':
        barcode = input("Enter barcode: ")
        params = {'barcode': barcode}
    elif choice == 'n':
        name = input("Enter product name: ")
        params = {'name': name}
    else:
        print("Invalid choice.")
        return

    resp = requests.get(f"{BASE_URL}/external/search", params=params)
    if resp.status_code == 200:
        data = resp.json()
        print("Product details from OpenFoodFacts:")
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print(f"Error: {resp.status_code} - {resp.text}")

def menu():
    while True:
        print("\n--- Inventory Management CLI ---")
        print("1. View all items")
        print("2. View one item (by ID)")
        print("3. Add new item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search external product info")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            view_all()
        elif choice == '2':
            item_id = input("Enter item ID: ")
            view_one(item_id)
        elif choice == '3':
            add_item()
        elif choice == '4':
            update_item()
        elif choice == '5':
            delete_item()
        elif choice == '6':
            search_external()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    try:
        requests.get(f"{BASE_URL}/inventory", timeout=2)
    except requests.exceptions.ConnectionError:
        print("ERROR: Flask server is not running. Please start app.py first.")
        sys.exit(1)
    menu()