from PyQt5 import QtWidgets, QtCore
from GUI import Ui_MainWindow
from utils import *
from bcrypt import hashpw, gensalt, checkpw

DB_FILE = "shop_management.db"

class App:
    def __init__(self):
        # Initialize application
        self.current_user = None
        self.current_user = None
        self.current_user_role = None
        self.current_user_email = None

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Initialize backend logic
        self.system = ShopManagementSystem()

        # Connect signals and slots
        self.setup_connections()

        # Starter point
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_4)
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_5)


    def setup_connections(self):

        # Login and Registration
        self.ui.pushButton_2.clicked.connect(self.login)  # Login
        self.ui.lineEdit.returnPressed.connect(self.login)
        self.ui.lineEdit_2.returnPressed.connect(self.login)
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_6))  # Register
        self.ui.pushButton_16.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_5))

        # Register new user
        self.ui.pushButton_15.clicked.connect(self.register_user)
        self.ui.lineEdit_3.returnPressed.connect(self.register_user)
        self.ui.lineEdit_4.returnPressed.connect(self.register_user)
        self.ui.lineEdit_7.returnPressed.connect(self.register_user)
        self.ui.lineEdit_8.returnPressed.connect(self.register_user)

        # Product Management
        self.ui.pushButton_3.clicked.connect(self.open_add_product_screen)  # Add Product
        self.ui.pushButton_18.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)) # Go Back

        #
        self.ui.pushButton_11.clicked.connect(self.open_add_product_screen)  # Update Product

        #PRODUCT VIEW
        self.ui.pushButton_4.clicked.connect(self.open_view_product)

        self.ui.pushButton_10.clicked.connect(self.delete_product)  # Delete Product

        # Sales Management
        self.ui.pushButton_13.clicked.connect(self.process_order)  # Process Sale
        self.ui.pushButton_12.clicked.connect(self.add_to_cart)  # Add to Cart

        # Reporting
        self.ui.pushButton_6.clicked.connect(self.generate_sales_report)  # Generate Report

    # Login User Function
    def login(self):
        email = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        # Validate email format
        if not is_valid_email(email):
            QtWidgets.QMessageBox.warning(self.MainWindow, "Invalid Email", "Please enter a valid email address!")
            return

        try:
            # Connect to the database
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Retrieve user information
            cursor.execute("SELECT full_name, role, email, password FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                full_name, role, email, hashed_password = user

                # Check the hashed password
                if hashed_password == self.system.hash_password(password):
                    self.current_user = full_name
                    self.current_user_role = role
                    self.current_user_email = email

                    if self.current_user_role == "Admin":
                        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
                        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_3)
                    elif self.current_user_role == "Employee":
                        # Redirect to employee dashboard
                        pass
                    # QtWidgets.QMessageBox.information(self.MainWindow, "Login Successful", f"Welcome, {self.current_user}!")
                else:
                    QtWidgets.QMessageBox.warning(self.MainWindow, "Login Failed", "Invalid email or password!")
            else:
                QtWidgets.QMessageBox.warning(self.MainWindow, "Login Failed", "Invalid email or password!")

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self.MainWindow, "Database Error", f"An error occurred: {e}")

    # Registration Functionality
    def register_user(self):
        full_name = self.ui.lineEdit_4.text()
        email = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_7.text()
        confirm_password = self.ui.lineEdit_8.text()

        # Check for password to match
        if password == "" or confirm_password == "" or full_name == "" or email == "":
            QtWidgets.QMessageBox.warning(self.MainWindow,
                                          "Registration Failed", "Cannot Proceed with empty password!")
            return

        # Check for password to match
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self.MainWindow, "Registration Failed", "Password not matched!")
            return

        self.system.register_user(full_name, email, password)
        QtWidgets.QMessageBox.information(self.MainWindow, "Registration",
                                          f"User {self.current_user}"
                                          f"Email: {self.current_user_email} registered successfully!")

    # Add Product Functionality
    def open_add_product_screen(self):

        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_6.clear()

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["Electronic", "Kitchen Accessories", "Toys"])
        self.ui.textEdit.clear()

        self.ui.label_12.clear()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        # name = self.ui.lineEdit_5.text()
        # category = self.ui.comboBox.currentText()
        # price = float(self.ui.lineEdit_6.text())
        # quantity = int(self.ui.lineEdit_9.text())
        # description = self.ui.textEdit.toPlainText()
        # self.system.add_product(name, category, price, description, quantity)
        # QtWidgets.QMessageBox.information(self.MainWindow, "Product Added", "Product added successfully!")

    # Update Product Functionality
    def update_product_screen(self):
        product_id = int(self.ui.lineEdit_10.text())
        # Logic for updating product will go here...
        QtWidgets.QMessageBox.information(self.MainWindow, "Product Update", "Product updated successfully!")

    # Delete Product Functionality
    def delete_product(self):
        product_id = int(self.ui.lineEdit_10.text())
        self.system.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
        self.system.conn.commit()
        QtWidgets.QMessageBox.information(self.MainWindow, "Product Deleted", "Product deleted successfully!")

    # Add to Cart
    def add_to_cart(self):
        # Logic for adding to cart will go here...
        pass

    # Process Sale
    def process_order(self):
        # Logic for processing sale will go here...
        pass

    # Generate Sales Report
    def generate_sales_report(self):
        # Logic for generating sales report will go here...
        pass

    def open_view_product(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_7)

    # def add_new_product(self):
    #     self.ui.stackedWidget.setCurrentWidget(self.ui.page)
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    starter = App()
    starter.MainWindow.show()
    sys.exit(app.exec_())
