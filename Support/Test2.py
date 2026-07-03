import sqlite3
from datetime import datetime

class ShopManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect("../shop_management.db")
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            date DATETIME NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )''')
        self.conn.commit()

    @staticmethod
    def hash_password(password):
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, full_name, email, password, role="Employee"):
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute("INSERT INTO users (full_name, email, password, role, created_at) VALUES (?, ?, ?, ?, ?)",
                               (full_name, email, hashed_password, role, datetime.now()))
            self.conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Email already exists. Please login.")

    def authenticate(self, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, self.hash_password(password)))
        user = self.cursor.fetchone()
        if user:
            return {"user_id": user[0], "full_name": user[1], "email": user[2], "role": user[4]}
        return None

    def add_product(self, name, category, price, description, quantity):
        self.cursor.execute("INSERT INTO products (name, category, price, description, quantity) VALUES (?, ?, ?, ?, ?)",
                           (name, category, price, description, quantity))
        self.conn.commit()
        print("Product added successfully!")

    def explore_and_update_product(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        print("\nProduct List:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Quantity: {product[5]}")

        product_id = int(input("Enter Product ID to update: "))
        self.cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        product = self.cursor.fetchone()
        if product:
            print("\n1. Update Name\n2. Update Price\n3. Update Description\n4. Update Quantity")
            choice = int(input("Choose an option: "))
            if choice == 1:
                new_name = input("Enter new name: ")
                self.cursor.execute("UPDATE products SET name = ? WHERE product_id = ?", (new_name, product_id))
            elif choice == 2:
                new_price = float(input("Enter new price: "))
                self.cursor.execute("UPDATE products SET price = ? WHERE product_id = ?", (new_price, product_id))
            elif choice == 3:
                new_description = input("Enter new description: ")
                self.cursor.execute("UPDATE products SET description = ? WHERE product_id = ?", (new_description, product_id))
            elif choice == 4:
                new_quantity = int(input("Enter new quantity: "))
                self.cursor.execute("UPDATE products SET quantity = ? WHERE product_id = ?", (new_quantity, product_id))
            self.conn.commit()
            print("Product updated successfully!")
        else:
            print("Product not found.")

    def view_current_stock(self):
        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()
        print("\nCurrent Stock:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}, Quantity: {product[5]}")

    def record_sale(self):
        product_id = int(input("Enter Product ID: "))
        quantity_sold = int(input("Enter Quantity Sold: "))
        self.cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        product = self.cursor.fetchone()
        if product:
            if product[5] < quantity_sold:
                print("Not enough stock.")
                return
            self.cursor.execute("UPDATE products SET quantity = quantity - ? WHERE product_id = ?", (quantity_sold, product_id))
            total_price = product[3] * quantity_sold
            self.cursor.execute("INSERT INTO sales (product_id, quantity, date, price) VALUES (?, ?, ?, ?)",
                               (product_id, quantity_sold, datetime.now(), total_price))
            self.conn.commit()
            print("Sale recorded successfully!")
        else:
            print("Product not found.")

    def generate_sales_report(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        self.cursor.execute("SELECT * FROM sales WHERE date BETWEEN ? AND ?", (start_date, end_date))
        sales = self.cursor.fetchall()

        print("\nSales Report:")
        total_revenue = 0
        for sale in sales:
            total_revenue += sale[4]
            print(f"Product ID: {sale[1]}, Quantity: {sale[2]}, Revenue: {sale[4]}")
        print(f"\nTotal Revenue: {total_revenue}")

    def main_menu(self):
        print("Welcome to Shop Management System")
        while True:
            print("\n1. Register\n2. Login\n3. Exit")
            choice = int(input("Choose an option: "))
            if choice == 1:
                full_name = input("Enter Full Name: ")
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                self.register_user(full_name, email, password, role="Admin")
            elif choice == 2:
                email = input("Enter Email: ")
                password = input("Enter Password: ")
                user = self.authenticate(email, password)
                if user:
                    print(f"Welcome {user['full_name']} ({user['role']})!")
                    while True:
                        print("\n1. Add Product\n2. Explore and Update Product\n3. View Current Stock\n4. Record Sale\n5. Generate Sales Report\n6. Logout")
                        action = int(input("Choose an option: "))
                        if action == 1:
                            name = input("Enter Product Name: ")
                            category = input("Enter Product Category: ")
                            price = float(input("Enter Product Price: "))
                            description = input("Enter Product Description: ")
                            quantity = int(input("Enter Product Quantity: "))
                            self.add_product(name, category, price, description, quantity)
                        elif action == 2:
                            self.explore_and_update_product()
                        elif action == 3:
                            self.view_current_stock()
                        elif action == 4:
                            self.record_sale()
                        elif action == 5:
                            self.generate_sales_report()
                        elif action == 6:
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

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    app = ShopManagementSystem()
    app.main_menu()
