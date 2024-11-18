import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class AddCustomerForm(ctk.CTkToplevel):
    def __init__(self, parent, db_conn, callback):
        super().__init__(parent)
        self.db_conn = db_conn
        self.callback = callback
        
        self.title("Add New Customer")
        self.geometry("500x400")
        
        # Make the window modal
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_bindings(self):
        # Bind Enter key to save
        self.bind('<Return>', lambda e: self.save_customer())
        self.bind('<Escape>', lambda e: self.destroy())
        
        # Add tab order
        self.name.bind('<Return>', lambda e: self.address.focus())
        self.address.bind('<Return>', lambda e: self.phone.focus())
        self.phone.bind('<Return>', lambda e: self.email.focus())
        self.email.bind('<Return>', lambda e: self.save_customer())
        
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Customer Information", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Form fields
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(fill="x")
        
        # Name
        name_frame = ctk.CTkFrame(fields_frame)
        name_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(name_frame, text="Name*:", font=("Arial", 12)).pack(side="left")
        self.name = ctk.CTkEntry(name_frame, width=300, font=("Arial", 12))
        self.name.pack(side="left", padx=5)
        
        # Address
        address_frame = ctk.CTkFrame(fields_frame)
        address_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(address_frame, text="Address:", font=("Arial", 12)).pack(side="left")
        self.address = ctk.CTkEntry(address_frame, width=300, font=("Arial", 12))
        self.address.pack(side="left", padx=5)
        
        # Phone
        phone_frame = ctk.CTkFrame(fields_frame)
        phone_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(phone_frame, text="Phone:", font=("Arial", 12)).pack(side="left")
        self.phone = ctk.CTkEntry(phone_frame, width=300, font=("Arial", 12))
        self.phone.pack(side="left", padx=5)
        
        # Email
        email_frame = ctk.CTkFrame(fields_frame)
        email_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(email_frame, text="Email:", font=("Arial", 12)).pack(side="left")
        self.email = ctk.CTkEntry(email_frame, width=300, font=("Arial", 12))
        self.email.pack(side="left", padx=5)
        
        # Required fields note
        note_frame = ctk.CTkFrame(fields_frame)
        note_frame.pack(fill="x", pady=10)
        note_label = ctk.CTkLabel(note_frame, text="* Required fields", 
                                font=("Arial", 12), text_color="red")
        note_label.pack(side="left")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        # Center the buttons
        button_container = ctk.CTkFrame(button_frame)
        button_container.pack(anchor="center")
        
        self.save_btn = ctk.CTkButton(button_container, text="Save (Enter)", 
                                    font=("Arial", 12),
                                    command=self.save_customer)
        self.save_btn.pack(side="left", padx=10)
        
        self.cancel_btn = ctk.CTkButton(button_container, text="Cancel (Esc)", 
                                      font=("Arial", 12),
                                      command=self.destroy)
        self.cancel_btn.pack(side="left", padx=10)
        
        # Set initial focus
        self.name.focus()
        
    def save_customer(self):
        name = self.name.get().strip()
        if not name:
            messagebox.showerror("Error", "Name is required!")
            self.name.focus()
            return
            
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO customers (name, address, phone, email)
                VALUES (?, ?, ?, ?)
            ''', (name, self.address.get(), self.phone.get(), self.email.get()))
            self.db_conn.commit()
            self.callback()  # Refresh the customer list
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {str(e)}")

class CustomerMaster(ctk.CTkFrame):
    def __init__(self, parent, db_conn, refresh_callback=None):
        super().__init__(parent)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.setup_ui()
        self.setup_bindings()
        
    def setup_bindings(self):
        # Bind keyboard shortcuts to the frame itself
        self.bind('<Control-n>', lambda e: self.show_add_form())
        self.bind('<Delete>', lambda e: self.delete_customer())
        
        # Bind Enter key to search entry
        self.search_entry.bind('<Return>', lambda e: self.on_search())
        
    def setup_ui(self):
        # Title and Add Button Frame
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="Customer Management", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(side="left")
        
        add_btn = ctk.CTkButton(header_frame, text="Add New Customer (Ctrl+N)", 
                               font=("Arial", 12),
                               command=self.show_add_form)
        add_btn.pack(side="right")
        
        # Search Frame
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        search_label = ctk.CTkLabel(search_frame, text="Search:", 
                                  font=("Arial", 12))
        search_label.pack(side="left", padx=5)
        
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.on_search)
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                       width=300, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=5)
        
        # Customer List Frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Header for customer list
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Column headers
        columns = [
            ("ID", 50),
            ("Name", 200),
            ("Address", 200),
            ("Phone", 150),
            ("Email", 200)
        ]
        
        for col, width in columns:
            ctk.CTkLabel(header_frame, text=col, width=width,
                        font=("Arial", 12, "bold")).pack(side="left", padx=2)
        
        # Scrollable frame for customer list
        self.customer_list = ctk.CTkScrollableFrame(list_frame)
        self.customer_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load customers
        self.load_customers()
        
    def show_add_form(self):
        def on_customer_added():
            self.load_customers()
            if self.refresh_callback:
                self.refresh_callback()
                
        AddCustomerForm(self, self.db_conn, on_customer_added)
            
    def delete_customer(self):
        # Get the selected customer frame
        for child in self.customer_list.winfo_children():
            if hasattr(child, 'selected') and child.selected:
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
                    customer_id = child.customer_id
                    cursor = self.db_conn.cursor()
                    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
                    self.db_conn.commit()
                    self.load_customers()
                    if self.refresh_callback:
                        self.refresh_callback()
                break
            
    def on_search(self, *args):
        search_term = self.search_var.get().lower()
        self.load_customers(search_term)
        
    def load_customers(self, search_term=''):
        # Clear existing customer list
        for widget in self.customer_list.winfo_children():
            widget.destroy()
            
        cursor = self.db_conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM customers 
                WHERE lower(name) LIKE ? OR lower(address) LIKE ? OR lower(phone) LIKE ? OR lower(email) LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM customers')
            
        for customer in cursor.fetchall():
            self.create_customer_row(customer)
            
    def create_customer_row(self, customer):
        # Create frame for customer row
        row = ctk.CTkFrame(self.customer_list)
        row.pack(fill="x", pady=2)
        row.customer_id = customer[0]  # Store customer ID
        row.selected = False  # Track selection state
        
        # Add customer details
        ctk.CTkLabel(row, text=str(customer[0]), width=50).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=customer[1], width=200).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=customer[2] or "", width=200).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=customer[3] or "", width=150).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=customer[4] or "", width=200).pack(side="left", padx=2)
        
        # Add selection handling
        def on_click(event):
            # Deselect all other rows
            for child in self.customer_list.winfo_children():
                if hasattr(child, 'selected'):
                    child.selected = False
                    child.configure(fg_color=("gray85", "gray25"))
            
            # Select this row
            row.selected = True
            row.configure(fg_color=("gray75", "gray35"))
            
        row.bind('<Button-1>', on_click)
        for widget in row.winfo_children():
            widget.bind('<Button-1>', on_click)
