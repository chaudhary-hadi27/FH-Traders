import hashlib
from datetime import datetime

# Database Simulation
db = {
    "users": [],  # Stores user data
    "products": [],  # Stores product data
    "sales": []  # Stores sales data
}

# Helper Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(email, password):
    for user in db['users']:
        if user['email'] == email and user['password'] == hash_password(password):
            return user
    return None

def register_user(full_name, email, password, role="Employee"):
    if any(user['email'] == email for user in db['users']):
        print("Email already exists. Please login.")
        return False
    hashed_password = hash_password(password)
    db['users'].append({
        "full_name": full_name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.now()
    })
    print("User registered successfully!")
    return True

def add_product(name, category, price, description, quantity):
    db['products'].append({
        "product_id": len(db['products']) + 1,
        "name": name,
        "category": category,
        "price": price,
        "description": description,
        "quantity": quantity
    })
    print("Product added successfully!")

def explore_and_update_product():
    print("\nProduct List:")
    for product in db['products']:
        print(f"ID: {product['product_id']}, Name: {product['name']}, Quantity: {product['quantity']}")

    product_id = int(input("Enter Product ID to update: "))
    for product in db['products']:
        if product['product_id'] == product_id:
            print("\n1. Update Name\n2. Update Price\n3. Update Description\n4. Update Quantity")
            choice = int(input("Choose an option: "))
            if choice == 1:
                product['name'] = input("Enter new name: ")
            elif choice == 2:
                product['price'] = float(input("Enter new price: "))
            elif choice == 3:
                product['description'] = input("Enter new description: ")
            elif choice == 4:
                product['quantity'] = int(input("Enter new quantity: "))
            print("Product updated successfully!")
            return
    print("Product not found.")

def record_sale():
    product_id = int(input("Enter Product ID: "))
    quantity_sold = int(input("Enter Quantity Sold: "))
    for product in db['products']:
        if product['product_id'] == product_id:
            if product['quantity'] < quantity_sold:
                print("Not enough stock.")
                return
            product['quantity'] -= quantity_sold
            sale = {
                "product_id": product_id,
                "quantity": quantity_sold,
                "date": datetime.now(),
                "price": product['price'] * quantity_sold
            }
            db['sales'].append(sale)
            print("Sale recorded successfully!")
            return
    print("Product not found.")

def generate_sales_report():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    print("\nSales Report:")
    total_revenue = 0
    for sale in db['sales']:
        if start_date <= sale['date'] <= end_date:
            total_revenue += sale['price']
            print(f"Product ID: {sale['product_id']}, Quantity: {sale['quantity']}, Revenue: {sale['price']}")
    print(f"\nTotal Revenue: {total_revenue}")

# Application Flow
def main():
    print("Welcome to Shop Management System")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = int(input("Choose an option: "))
        if choice == 1:
            full_name = input("Enter Full Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            register_user(full_name, email, password, role="Admin")
        elif choice == 2:
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            user = authenticate(email, password)
            if user:
                print(f"Welcome {user['full_name']} ({user['role']})!")
                while True:
                    print("\n1. Add Product\n2. Explore and Update Product\n3. Record Sale\n4. Generate Sales Report\n5. Logout")
                    action = int(input("Choose an option: "))
                    if action == 1:
                        name = input("Enter Product Name: ")
                        category = input("Enter Product Category: ")
                        price = float(input("Enter Product Price: "))
                        description = input("Enter Product Description: ")
                        quantity = int(input("Enter Product Quantity: "))
                        add_product(name, category, price, description, quantity)
                    elif action == 2:
                        explore_and_update_product()
                    elif action == 3:
                        record_sale()
                    elif action == 4:
                        generate_sales_report()
                    elif action == 5:
                        print("Logged out.")
                        break
                    else:
                        print("Invalid option.")
            else:
                print("Invalid credentials.")
        elif choice == 3:
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
