"""
python final exam, phitron batch 5
by Anup Barua, 21.5.25
github code: https://github.com/anup-sdp/python_restaurant_management_system/blob/main/main.py
"""

from abc import ABC  # abstract base class

print("--- Welcome to Restaurant Management System ---\n")


class User(ABC):
    def __init__(self, name):
        self.name = name


class Customer(User):
    def __init__(self, name, email, address):
        super().__init__(name)  # customer Username, must be unique
        self.email = email
        self.address = address
        self.balance = 0
        self.past_orders = []  # list of FoodItem class

    def view_menu(self, restaurant):
        restaurant.view_menu_items()
    def view_balance(self):
        print(f"your balance is: {self.balance:.2f}")    
    def add_balance(self, amount):
        if amount <= 0:
            print("Amount must be positive.")
            return
        self.balance += amount
        print(f"your current balance is: {self.balance:.2f}") 
    def place_order(self, restaurant):
        restaurant.view_menu_items()
        try:
            choice = int(input("Select food item number from above menu list: "))    
            if choice < 1 or choice > restaurant.menu_item_count():
                print("Choice out of range. try again")
                return
        except ValueError:
            print("Invalid input. Please try again with valid number.")
            return
            
        food_item = restaurant.get_menu_item(choice-1)  # index = choice-1
        if food_item.quantity <= 0:
            print("Item out of stock.")
            return
        if self.balance < food_item.price:
            print("Insufficient balance. Please add funds.")
            return
        self.balance -= food_item.price
        self.past_orders.append(food_item)
        food_item.quantity -= 1
        print(f"Order placed for {food_item.name}. your remaining balance: {self.balance:.2f}")
        
    def view_past_orders(self, restaurant):
        if len(self.past_orders) == 0:
            print("There are no past orders of you")
            return
        print("*** past orders ***")
        print("food item\tprice")
        for order in self.past_orders:
            print(f"{order.name}\t{order.price}")            
         


class Admin(User):
    def __init__(self, name):
        super().__init__(name)

    def add_customer(self, restaurant):
        print("To create a new Customer, please enter the info:")
        user_name = input("customer user name (unique): ")
        customer_email = input("customer email: ")
        customer_address = input("customer address: ")
        customer = Customer(name=user_name, email=customer_email, address=customer_address)
        customer.add_balance(1000) # give initial balance 1000 tk
        created = restaurant.add_customer(customer)
        if created:
            print(f"Customer {user_name} created with an initial balance of 1000 TK.")

    def remove_customer(self, restaurant):
        user_name = input("To remove a customer, enter his/her name :")
        restaurant.remove_customer(user_name)

    def view_all_customers(self, restaurant):
        restaurant.view_all_customers()

        
    def manage_restaurant_food_menu(self, restaurant):
        while True:            
            print("Select an option: ")
            print("1. view all food items") 
            print("2. add a food item to menu")
            print("3. remove a food item from menu")
            print("4. update a food menu price")
            print("5. update a food menu quantity/stock")
            print("6. go to previous menu")
            print()
            choice = input("Select any number: ")
            print()
            if choice == '1':
                restaurant.view_menu_items()
            elif choice == '2':
                restaurant.add_menu_item()
            elif choice == '3':
                restaurant.remove_menu_item()
            elif choice == '4':
                restaurant.update_menu_price()
            elif choice == '5':
                restaurant.update_menu_quantity()
            elif choice == '6':
                break
            else:
                print("Invalid Choice, try again.\n")	


class FoodItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity  # available quantity / stock
        
    def __str__ (self):
        return f"{self.name}\t{self.price}\t{self.quantity}"	


class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = []  # list of FoodItem class
        self.customers = []  # list of Customer class

    def add_customer(self, customer):  # can non admin add ?       
        for cus in self.customers:
            if cus.name.lower() == customer.name.lower():
                print(f"this customer name :{customer.name} already exists! try again please.")
                return False
        self.customers.append(customer)
        return True

    def remove_customer(self, user_name):
        exists = False
        for cus in self.customers:
            if cus.name.lower() == user_name.lower():
                exists = True
                self.customers.remove(cus)
                print(f"The customer named :{user_name} removed.")
        if not exists:
            print(f"Found no customer named :{user_name}!")

    def view_all_customers(self):
        if len(self.customers) == 0:
            print("No customers added to list!")
            return
        print("All Customers:")
        print("username\temail\taddress")
        for cus in self.customers:
            print(f"{cus.name}\t{cus.email}\t{cus.address}")

    def get_customer_by_name(self, cus_name):
        for cus in self.customers:
            if cus.name.lower() == cus_name.lower():
                return cus
        return None
    
    def view_menu_items(self):
        if len(self.menu) == 0:
            print("No food items available at the moment")
            return
        print("*** Food Menu Items ***")
        print(f"No.\tname\tprice\tstock quantity") 
        for index,item in enumerate(self.menu, start=1):
            print(f"{index}. {item}")  # item == each FoodItem
        print()    
            
    def menu_item_count(self):
        return len(self.menu)

    def add_menu_item(self):  # add new item to menu
        print("Enter the following info for adding food item")
        name = input("Enter food item name: ")
        price = float(input("enter price: "))
        quantity = int(input("enter stock/quantity: "))
        food_item = FoodItem(name, price, quantity)
        self.menu.append(food_item)
        
    def get_menu_item(self, idx):
        if 0<= idx < len(self.menu):
            return self.menu[idx]  # return the menu item
        else:
            print("index out of range")
            return None
        
    def remove_menu_item(self):
        print("Which food item to remove (select number): ")
        self.view_menu_items()
        try:
            choice = int(input("choice = "))
            if choice<1 or choice>len(self.menu):
                raise ValueError
        except ValueError:
            print('Invalid input, try again later.')
            return
        #del self.menu[choice-1]
        item = self.menu.pop(choice-1) # ---
        print(f'Food item "{item.name}" removed.')
        
    def update_menu_price(self):
        print("which food items price to update (select number): ")
        self.view_menu_items()
        try:
            choice = int(input("choice = "))
            if choice<1 or choice>len(self.menu):
                raise ValueError
        except ValueError:
            print('Invalid input, try again later.') 
            return
        try:
            new_price = float(input('enter new price : '))
            if new_price<0:
                raise ValueError
            self.menu[choice-1].price = new_price
        except ValueError:
            print('Invalid input, try again later.')   
            return 
            
    def update_menu_quantity(self):
        print("which food items quantity/stock to update (select number): ")
        self.view_menu_items()
        try:
            choice = int(input("choice = "))
            if choice<1 or choice>len(self.menu):
                raise ValueError
        except ValueError:
            print('Invalid input, try again later.')
            return
        try:
            new_quantity = int(input('enter new quantity/stock : '))
            if new_quantity<0:
                raise ValueError
            self.menu[choice-1].quantity= new_quantity
        except ValueError:
            print('Invalid input, try again later.')
            return    

    

# ---------------------------------------------------------------

our_restaurant = Restaurant("Mamar Hotel")
# add demo food items
our_restaurant.menu.append(FoodItem("Burger", 150, 80))
our_restaurant.menu.append(FoodItem("Sandwich", 120, 80))
our_restaurant.menu.append(FoodItem("Tea", 20, 500))
our_restaurant.menu.append(FoodItem("Coffee", 100, 200))
admin = None


def print_admin_menu():
    print(f"--- Admin Menu - {our_restaurant.name} ---")
    print("Please Select an option from below :")
    print("1. Create Customer Account")
    print("2. Remove Customer Account")
    print("3. View All Customers")
    print("4. Manage Restaurant Food Menu")
    print("5. go to Main Menu")
    print()


def admin_menu():
    global admin
    if not admin:
        admin_name = input("Enter Admin name: ")
        admin = Admin(admin_name)
    print(f"Welcome Admin, {admin.name}\n")
    while True:
        print_admin_menu()
        choice = input("Select any number: ")
        print()
        if choice == "1":
            admin.add_customer(our_restaurant)
        elif choice == "2":
            admin.remove_customer(our_restaurant)
        elif choice == "3":
            admin.view_all_customers(our_restaurant)
        elif choice == "4":
            #our_restaurant.manage_restaurant_food_menu() -------------------------------------------------------------
            admin.manage_restaurant_food_menu(our_restaurant)
        elif choice == "5":            
            break
        else:
            print("Invalid Choice, try again.")


def print_customer_menu(customer_name):
    print()
    print(f"--- {customer_name}'s Menu ---")
    print("Please Select an option from below :")
    print("1. View Restaurant Menu")  # food options
    print("2. View My Balance")
    print("3. Add Balance")
    print("4. Place Order")
    print("5. View Past Orders")
    print("6. go to Main Menu")
    print()


def customer_menu():
    cus_name = input("Enter Customer name: ")
    customer = our_restaurant.get_customer_by_name(cus_name)
    if not customer:  # customer == None
        print(f"No customer by name {cus_name} found! try again.")
        return
    while True:
        print_customer_menu(cus_name)
        choice = input("Select any number: ")
        print()
        if choice == "1":
            our_restaurant.view_menu_items()
        elif choice == '2':
            customer.view_balance()
        elif choice == '3':
            while True: # ---
                try:
                    amount = float(input("Enter amount to add: "))
                    customer.add_balance(amount)
                except ValueError:
                    print("Invalid input. Try again.")
        elif choice == '4':
            customer.place_order(our_restaurant)
        elif choice == '5':
            customer.view_past_orders(our_restaurant)
        elif choice == '6':
            break
        else:
            print("Invalid Choice, try again.\n")


def run_program():
    while True:
        # Main Menu
        print("Please Select an option from below :")
        print("1. Admin Menu")
        print("2. Customer Menu")
        print("3. Exit Program")
        print()
        choice = input("Select any number: ")
        print()
        if choice == "1":
            admin_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Thank You for using our App!\n")
            break
        else:
            print("Invalid Choice, try again.\n")


run_program()
