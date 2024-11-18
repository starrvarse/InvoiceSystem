import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from modern_combobox import ModernSearchableCombobox
from invoice_printer import InvoicePrinter

class InvoicePage(ctk.CTkFrame):
    def __init__(self, parent, db_conn):
        super().__init__(parent)
        self.db_conn = db_conn
        
        # Variables
        self.items = []
        self.total_amount = ctk.StringVar(value="0.00")
        self.selected_customer = None
        self.price_type = ctk.StringVar(value="retail")  # Default to retail price
        
        self.setup_ui()
        self.setup_bindings()
        
    def setup_bindings(self):
        # Keyboard shortcuts - bind to frame instead of globally
        self.bind('<Control-s>', lambda e: self.generate_invoice())
        self.bind('<Control-a>', lambda e: self.add_item())
        self.bind('<Control-n>', lambda e: self.clear_all())
        
        # Navigation bindings
        self.customer_cb.bind('<Return>', lambda e: self.on_customer_selected())
        self.product_cb.bind('<Return>', lambda e: self.quantity.focus())
        
        # Fix: Bind Return key to add_item for quantity field and ensure it works
        self.quantity.bind('<Return>', lambda e: (self.add_item(), 'break'))
        
        # Tree bindings
        self.tree.bind('<Delete>', lambda e: self.remove_item())
        self.tree.bind('<Return>', lambda e: self.focus_product_entry())
        
        # Add button binding
        self.add_btn.bind('<Return>', lambda e: self.add_item())

    def focus_product_entry(self):
        self.product_cb.focus()
        
    def setup_ui(self):
        # Title with shortcuts
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        title_text = "Create New Invoice (Ctrl+S: Save, Ctrl+A: Add Item, Ctrl+N: New)"
        title_label = ctk.CTkLabel(title_frame, text=title_text, font=("Arial", 16, "bold"))
        title_label.pack(side="left")
        
        # Customer Selection Frame
        self.create_customer_selection_frame()
        
        # Items Frame
        self.create_items_frame()
        
        # Summary Frame
        self.create_summary_frame()

    def create_customer_selection_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=5)
        
        header = ctk.CTkLabel(frame, text="Customer Information (Optional)", 
                            font=("Arial", 14, "bold"))
        header.pack(pady=(5,10))
        
        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Customer selection
        ctk.CTkLabel(input_frame, text="Select/Search Customer:", 
                    font=("Arial", 12)).pack(side="left", padx=5)
        self.customer_cb = ModernSearchableCombobox(input_frame, width=300, font=("Arial", 12))
        self.customer_cb.pack(side="left", padx=5)
        
        # Customer details display
        self.customer_details = ctk.CTkLabel(input_frame, text="", font=("Arial", 12))
        self.customer_details.pack(side="left", padx=20)
        
        self.load_customers()

    def create_items_frame(self):
        items_frame = ctk.CTkFrame(self)
        items_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        header = ctk.CTkLabel(items_frame, text="Items", font=("Arial", 14, "bold"))
        header.pack(pady=(5,10))
        
        # Create main container for table and input
        main_container = ctk.CTkFrame(items_frame)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create table frame
        table_frame = ctk.CTkFrame(main_container)
        table_frame.pack(fill="both", expand=True)
        
        # Items table (using ttk.Treeview as CTk doesn't have a direct equivalent)
        columns = ('Product', 'Quantity', 'Unit Price', 'Price Type', 'Total')
        self.tree = ctk.CTkScrollableFrame(table_frame)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create headers with modified widths
        header_frame = ctk.CTkFrame(self.tree)
        header_frame.pack(fill="x", pady=(0, 5))
        
        widths = {
            'Product': 300, 
            'Quantity': 100, 
            'Unit Price': 100,
            'Price Type': 100, 
            'Total': 100
        }
        
        for col in columns:
            ctk.CTkLabel(
                header_frame, 
                text=col, 
                font=("Arial", 12, "bold"),
                width=widths[col]
            ).pack(side="left", padx=2)
        
        # Create input frame at the bottom
        input_frame = ctk.CTkFrame(main_container)
        input_frame.pack(fill="x", pady=(10, 0))
        
        # Product selection with modern searchable combobox
        ctk.CTkLabel(input_frame, text="Product:", 
                    font=("Arial", 12)).pack(side="left", padx=5)
        self.product_cb = ModernSearchableCombobox(input_frame, width=400, font=("Arial", 12))
        self.product_cb.pack(side="left", padx=5)
        
        # Price Type selection
        ctk.CTkLabel(input_frame, text="Price Type:", 
                    font=("Arial", 12)).pack(side="left", padx=5)
        self.price_type = ctk.CTkOptionMenu(input_frame, width=100, font=("Arial", 12),
                                          values=["Wholesale", "Retail"])
        self.price_type.set("Retail")
        self.price_type.pack(side="left", padx=5)
        
        # Quantity entry
        ctk.CTkLabel(input_frame, text="Qty:", 
                    font=("Arial", 12)).pack(side="left", padx=5)
        self.quantity = ctk.CTkEntry(input_frame, width=80, font=("Arial", 12))
        self.quantity.pack(side="left", padx=5)
        
        # Add button
        self.add_btn = ctk.CTkButton(input_frame, text="Add (Enter)",
                                   font=("Arial", 12),
                                   command=self.add_item)
        self.add_btn.pack(side="left", padx=5)
        
        # Shortcuts info
        shortcuts_frame = ctk.CTkFrame(main_container)
        shortcuts_frame.pack(fill="x", pady=(10, 0))
        ctk.CTkLabel(shortcuts_frame, 
                    text="Tab/Enter: Navigate • Delete: Remove Item • Type to Search",
                    font=("Arial", 11),
                    text_color="gray").pack(side="left")
        
        self.load_products()

    def create_item_row(self, item_data):
        """Create a new row in the items table with editing capability."""
        frame = ctk.CTkFrame(self.tree)
        frame.pack(fill="x", pady=2)
        frame.item_data = item_data

        # Product name (non-editable)
        product_label = ctk.CTkLabel(
            frame, 
            text=item_data[0],
            width=300,
            anchor="w"
        )
        product_label.pack(side="left", padx=2)

        # Quantity (editable)
        quantity_entry = ctk.CTkEntry(frame, width=100)
        quantity_entry.insert(0, str(item_data[1]))
        quantity_entry.pack(side="left", padx=2)
        
        # Unit Price (editable)
        price_entry = ctk.CTkEntry(frame, width=100)
        price_entry.insert(0, str(item_data[4]))
        price_entry.pack(side="left", padx=2)

        # Price Type (non-editable)
        price_type_label = ctk.CTkLabel(
            frame, 
            text=item_data[3],
            width=100
        )
        price_type_label.pack(side="left", padx=2)

        # Total (auto-calculated)
        total_label = ctk.CTkLabel(
            frame, 
            text=f"₹{item_data[5]:.2f}",
            width=100
        )
        total_label.pack(side="left", padx=2)

        # Delete button
        delete_btn = ctk.CTkButton(
            frame,
            text="×",
            width=30,
            height=24,
            command=lambda: self.remove_item(frame)
        )
        delete_btn.pack(side="left", padx=(5, 0))

        # Update total when quantity or price changes
        def update_total(*args):
            try:
                qty = float(quantity_entry.get())
                price = float(price_entry.get())
                new_total = qty * price
                total_label.configure(text=f"₹{new_total:.2f}")
                frame.item_data = (
                    item_data[0], qty, item_data[2],
                    item_data[3], price, new_total
                )
                self.update_total_amount()
            except ValueError:
                pass

        # Bind entry changes
        quantity_entry.bind('<KeyRelease>', update_total)
        price_entry.bind('<KeyRelease>', update_total)
        
        return frame

    def create_summary_frame(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Total amount
        total_frame = ctk.CTkFrame(frame)
        total_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(total_frame, text="Total Amount: ₹", 
                    font=("Arial", 14, "bold")).pack(side="left")
        ctk.CTkLabel(total_frame, textvariable=self.total_amount, 
                    font=("Arial", 14, "bold")).pack(side="left")
        
        # Buttons
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(side="right", padx=10)
        
        self.generate_btn = ctk.CTkButton(button_frame, 
                                        text="Generate Invoice (Ctrl+S)",
                                        font=("Arial", 12),
                                        command=self.generate_invoice)
        self.generate_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(button_frame, 
                                     text="New Invoice (Ctrl+N)",
                                     font=("Arial", 12),
                                     command=self.clear_all)
        self.clear_btn.pack(side="left", padx=5)
        
    def validate_quantity(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def remove_item(self, item_frame):
        """Remove an item from the invoice."""
        item_frame.destroy()
        self.update_total_amount()
            
    def load_customers(self):
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
        values = [f"{c[0]} - {c[1]}" for c in customers]
        self.customer_cb.set_values(values)
        
    def load_products(self):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT id, name, wholesale_price, retail_price, base_unit FROM products')
            products = cursor.fetchall()
            if products:
                values = []
                for p in products:
                    try:
                        wholesale = float(p[2]) if p[2] is not None else 0.0
                        retail = float(p[3]) if p[3] is not None else 0.0
                        base_unit = p[4] if p[4] is not None else "Unit"
                        values.append(f"{p[0]} - {p[1]} (W:₹{wholesale:.2f}, R:₹{retail:.2f})")
                    except (ValueError, TypeError):
                        continue
                self.product_cb.set_values(values)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
            self.product_cb.set_values([])
            
    def on_customer_selected(self, event=None):
        if not self.customer_cb.get():
            self.selected_customer = None
            self.customer_details.configure(text="")
            return
            
        try:
            customer_id = int(self.customer_cb.get().split(' - ')[0])
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            customer = cursor.fetchone()
            
            if customer:
                self.selected_customer = customer
                details = f"Address: {customer[2] or 'N/A'} | Phone: {customer[3] or 'N/A'}"
                self.customer_details.configure(text=details)
                self.product_cb.focus()
            else:
                self.selected_customer = None
                self.customer_details.configure(text="")
                messagebox.showerror("Error", "Selected customer not found in database")
        except (ValueError, IndexError):
            self.selected_customer = None
            self.customer_details.configure(text="")
            messagebox.showerror("Error", "Invalid customer selection format")
        
    def add_item(self):
        """Modified add_item method to use the new row creation."""
        # Validate inputs as before
        if not self.product_cb.get() or not self.quantity.get():
            messagebox.showerror("Error", "Please select a product and enter quantity")
            if not self.product_cb.get():
                self.product_cb.focus()
            else:
                self.quantity.focus()
            return

        try:
            product_id = int(self.product_cb.get().split(' - ')[0])
            quantity = float(self.quantity.get())
            price_type = self.price_type.get()
            
            # Basic validation
            if quantity <= 0:
                messagebox.showerror("Error", "Please enter a valid quantity greater than 0")
                self.quantity.focus()
                return

            cursor = self.db_conn.cursor()
            cursor.execute(
                'SELECT id, name, wholesale_price, retail_price, base_unit FROM products WHERE id = ?', 
                (product_id,)
            )
            product = cursor.fetchone()

            if product:
                # Get price based on type
                if price_type.lower() == "wholesale":
                    price = float(product[2]) if product[2] is not None else 0.0
                else:
                    price = float(product[3]) if product[3] is not None else 0.0

                if price <= 0:
                    messagebox.showerror("Error", f"Invalid {price_type.lower()} price for the selected product")
                    return

                # Check for duplicate
                for widget in self.tree.winfo_children():
                    if (hasattr(widget, 'item_data') and 
                        widget.item_data[0] == product[1] and 
                        widget.item_data[3] == price_type):
                        messagebox.showerror("Error", "Product already added with the same price type")
                        return

                # Create new row
                item_data = (
                    product[1], quantity, product[4],
                    price_type, price, quantity * price
                )
                self.create_item_row(item_data)
                self.update_total_amount()

                # Clear inputs
                self.quantity.delete(0, "end")
                self.product_cb.set('')
                self.product_cb.focus()

        except ValueError as e:
            messagebox.showerror("Error", "Please enter a valid quantity")
            self.quantity.focus()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
    def update_total_amount(self):
        """Update the total amount based on all items."""
        total = 0
        for widget in self.tree.winfo_children():
            if hasattr(widget, 'item_data'):
                total += widget.item_data[5]
        self.total_amount.set(f"{total:.2f}")

    def get_all_items(self):
        """Get all items from the tree for invoice generation."""
        items = []
        # Skip the header frame (first child)
        for widget in list(self.tree.winfo_children())[1:]:
            if hasattr(widget, 'item_data'):
                items.append(widget.item_data)
        return items

    def generate_invoice(self):
        """Generate invoice PDF with current items."""
        # Get all items from the tree
        items = self.get_all_items()
        
        if not items:
            messagebox.showerror("Error", "No items added to invoice")
            self.product_cb.focus()
            return False
            
        try:
            printer = InvoicePrinter()
            pdf_file = printer.generate_pdf(
                self.selected_customer,
                items,  # Use items from tree instead of self.items
                float(self.total_amount.get())
            )
            
            messagebox.showinfo(
                "Success",
                f"Invoice generated successfully!\nSaved as: {pdf_file}"
            )
            self.clear_all()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")
            return False

    def clear_all(self):
        self.customer_cb.set('')
        self.customer_details.configure(text="")
        self.selected_customer = None
        self.product_cb.set('')
        self.quantity.delete(0, "end")
        self.price_type.set("Retail")
        
        # Clear items from scrollable frame
        for widget in self.tree.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.tree.winfo_children()[0]:
                widget.destroy()
                
        self.items.clear()
        self.total_amount.set("0.00")
        self.customer_cb.focus()
        
    def refresh(self):
        self.load_customers()
        self.load_products()
