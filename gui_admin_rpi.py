import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector  # Import mysql.connector

# Establishing MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="Atmart_DB",
    passwd="login12DB",
    database="foodpurchasinghistory"
)

if mydb.is_connected():
    print('connected')

cursor = mydb.cursor()

sql_insert_or_update = """
INSERT INTO stock_details (Item_Name, Stock) 
VALUES (%s, %s) 
ON DUPLICATE KEY UPDATE Stock = Stock + VALUES(Stock)
"""

sql_select_details = "SELECT Item_Name, Stock FROM stock_details WHERE Stock < 10"
sql_select_recent_purchases = "SELECT id,item_name, weight, price_per_kg, total_price FROM history"

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        tk.Label(self, text="Admin Name:").pack(pady=5)
        self.admin_name_entry = tk.Entry(self)
        self.admin_name_entry.pack(pady=5)

        tk.Label(self, text="Admin ID:").pack(pady=5)
        self.admin_id_entry = tk.Entry(self)
        self.admin_id_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def login(self):
        admin_name = self.admin_name_entry.get()
        admin_id = self.admin_id_entry.get()

        if admin_name == '' and admin_id == '':
            self.destroy()
            app = AdminInterface(admin_name, admin_id)
            app.mainloop()
        else:
            messagebox.showwarning("Login Failed", "Incorrect Admin Name or Admin ID")

class AdminInterface(tk.Tk):
    def __init__(self, admin_name, admin_id):
        super().__init__()

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.title("Admin Interface")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")  # Adjusted size to 90% of screen

        # Admin Interface Label
        admin_label = tk.Label(self, text="Admin Interface", font=("Arial", 16))
        admin_label.pack(pady=10, anchor='w')

        # Admin details
        admin_details_frame = tk.Frame(self, borderwidth=2, relief="solid", padx=10, pady=10)
        admin_details_frame.pack(pady=10, anchor='w', fill='x')
        admin_details_label = tk.Label(admin_details_frame, text=f"Admin Name: {admin_name}\nAdmin ID: {admin_id}")
        admin_details_label.pack(anchor='w')

        # Logo
        logo_image_path = r"/home/asus/Desktop/Interface/guienv/lib/python3.11/site-packages/Logo_of_IIT_Bhilai.png"
        self.logo_image = Image.open(logo_image_path)
        self.logo_image = self.logo_image.resize((80, 80), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        logo_label = tk.Label(self, image=self.logo_photo)
        logo_label.place(x=int(screen_width * 0.9) - 100, y=10, width=80, height=80)

        # Separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', pady=10)

        # Frames for each section
        recent_purchases_frame = tk.Frame(self, borderwidth=2, relief="solid")
        recent_purchases_frame.place(x=20, y=180, width=(int(screen_width * 0.9) - 60) // 2,
                                     height=(int(screen_height * 0.9) - 200) // 2)
        stock_details_frame = tk.Frame(self, borderwidth=2, relief="solid")
        stock_details_frame.place(x=40 + (int(screen_width * 0.9) - 60) // 2, y=180,
                                  width=(int(screen_width * 0.9) - 60) // 2,
                                  height=(int(screen_height * 0.9) - 200) // 2)
        image_capture_frame = tk.Frame(self, borderwidth=2, relief="solid")
        image_capture_frame.place(x=20, y=200 + (int(screen_height * 0.9) - 200) // 2,
                                  width=(int(screen_width * 0.9) - 60) // 2,
                                  height=(int(screen_height * 0.9) - 200) // 2)
        stock_update_frame = tk.Frame(self, borderwidth=2, relief="solid")
        stock_update_frame.place(x=40 + (int(screen_width * 0.9) - 60) // 2,
                                 y=200 + (int(screen_height * 0.9) - 200) // 2,
                                 width=(int(screen_width * 0.9) - 60) // 2,
                                 height=(int(screen_height * 0.9) - 200) // 2)

        # Section titles
        recent_purchases_label = tk.Label(self, text="Recent Purchases", font=("Arial", 14))
        recent_purchases_label.place(x=20, y=150)
        stock_details_label = tk.Label(self, text="Stock details", font=("Arial", 14))
        stock_details_label.place(x=40 + (int(screen_width * 0.9) - 60) // 2, y=150)
        image_capture_label = tk.Label(self, text="Image Capture", font=("Arial", 14))
        image_capture_label.place(x=20, y=170 + (int(screen_height * 0.9) - 200) // 2)
        stock_update_label = tk.Label(self, text="Stock update", font=("Arial", 14))
        stock_update_label.place(x=40 + (int(screen_width * 0.9) - 60) // 2,
                                 y=170 + (int(screen_height * 0.9) - 200) // 2)

        # Content inside frames
        # Recent Purchases Table
        self.recent_purchases_table = ttk.Frame(recent_purchases_frame)
        self.recent_purchases_table.pack(expand=True, fill='both', padx=10, pady=10)

        self.create_recent_purchases_table()

        # Stock Details Table
        self.stock_details_table = ttk.Frame(stock_details_frame)
        self.stock_details_table.pack(expand=True, fill='both', padx=10, pady=10)

        self.create_stock_details_table()

        # Stock Update
        tk.Label(stock_update_frame, text="Fruit/Vegetable Name:").pack(pady=5)
        self.stock_name_combobox = ttk.Combobox(stock_update_frame, values=["Apple", "Banana", "Orange"], width=30)
        self.stock_name_combobox.pack(pady=5)

        tk.Label(stock_update_frame, text="Quantity:").pack(pady=5)
        self.stock_quantity_entry = tk.Entry(stock_update_frame, width=30)
        self.stock_quantity_entry.pack(pady=5)

        confirm_button = tk.Button(stock_update_frame, text="Confirm", command=self.update_stock)
        confirm_button.pack(pady=5)
        Refresh = tk.Button(stock_update_frame, text="Refresh", command=self.update_stock_2)
        Refresh.pack(pady=5)

        # Load data from database
        self.load_stock_data()
        self.load_recent_purchases_data()  # Load recent purchases data
        self.after(2000,self.update_stock_2)

    def create_recent_purchases_table(self):
        columns = ['Transaction_No','Item Name', 'Weight', 'Price per kg', 'Total Price']

        for col, text in enumerate(columns):
            label = tk.Label(self.recent_purchases_table, text=text, borderwidth=2, relief="groove", width=2)
            label.grid(row=0, column=col, sticky='nsew')

        self.recent_purchases_data = []
        
        for i in range(15):  # Create 15 rows
            row_entries = []
            for j in range(5):
                frame = tk.Frame(self.recent_purchases_table, borderwidth=2, relief="groove")
                frame.grid(row=i + 1, column=j, sticky='nsew')
                entry = tk.Entry(frame, borderwidth=0)
                entry.pack(expand=True, fill='both')
                row_entries.append(entry)
            self.recent_purchases_data.append(row_entries)

        for i in range(5):
            self.recent_purchases_table.columnconfigure(i, weight=1)
        for i in range(16):  # Include header row
            self.recent_purchases_table.rowconfigure(i, weight=1)
            

    def create_stock_details_table(self):
        columns = ['Item Name', 'Present Stock']

        for col, text in enumerate(columns):
            label = tk.Label(self.stock_details_table, text=text, borderwidth=2, relief="groove", width=20)
            label.grid(row=0, column=col, sticky='nsew')

        self.table_data = []

        for i in range(15):  # Create 15 rows
            row_entries = []
            for j in range(2):  # Changed from 4 to 2
                frame = tk.Frame(self.stock_details_table, borderwidth=2, relief="groove")
                frame.grid(row=i + 1, column=j, sticky='nsew')
                entry = tk.Entry(frame, borderwidth=0)
                entry.pack(expand=True, fill='both')
                row_entries.append(entry)
            self.table_data.append(row_entries)

        for i in range(2):  # Changed from 4 to 2
            self.stock_details_table.columnconfigure(i, weight=1)
        for i in range(16):  # Include header row
            self.stock_details_table.rowconfigure(i, weight=1)

    def load_stock_data(self):
        cursor.execute(sql_select_details)
        rows = cursor.fetchall()

        # Clear existing data
        for row_entries in self.table_data:
            for entry in row_entries:
                entry.delete(0, tk.END)

        # Insert new data
        row_count = len(rows)
        for idx in range(row_count):
            row = rows[row_count - 1 - idx]
            if idx < len(self.table_data):
                self.table_data[idx][0].insert(0, row[0])  # Assuming first column is Item_Name
                self.table_data[idx][1].insert(0, row[1])  # Assuming second column is Stock

    def load_recent_purchases_data(self):
        cursor.execute(sql_select_recent_purchases)
        rows = cursor.fetchall()

        # Clear existing data
        for row_entries in self.recent_purchases_data:
         for entry in row_entries:
            entry.delete(0, tk.END)

     # Insert new data, iterating from the back
        row_count = len(rows)
        for idx in range(row_count):
          row = rows[row_count - 1 - idx]
          if idx < len(self.recent_purchases_data):
            self.recent_purchases_data[idx][0].insert(0, row[0]) 
            self.recent_purchases_data[idx][1].insert(0, row[1]) 
            self.recent_purchases_data[idx][2].insert(0, row[2])  
            self.recent_purchases_data[idx][3].insert(0, row[3])  
            self.recent_purchases_data[idx][4].insert(0, row[4])  


    def update_stock(self):
        stock_name = self.stock_name_combobox.get()
        stock_quantity = self.stock_quantity_entry.get()

        if stock_name and stock_quantity:
            try:
                cursor.execute(sql_insert_or_update, (stock_name, stock_quantity))
                mydb.commit()
                self.load_stock_data()  # Reload the data to reflect the update
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating stock: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter both stock name and quantity")
                        
    def update_stock_2(self):
                mydb.commit()
                self.load_stock_data()
                self.load_recent_purchases_data()
                self.after(2000,self.update_stock_2)

if __name__ == "__main__":
    
    login_page = LoginPage()
    login_page.mainloop()
