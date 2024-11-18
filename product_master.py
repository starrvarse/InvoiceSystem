import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import pandas as pd

class AddProductForm(ctk.CTkToplevel):
    def __init__(self, parent, db_conn, callback):
        super().__init__(parent)
        self.db_conn = db_conn
        self.callback = callback
        
        self.title("Add New Product")
        self.geometry("600x700")
        
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
        self.bind('<Return>', lambda e: self.save_product())
        self.bind('<Escape>', lambda e: self.destroy())
        
        # Add tab order
        self.name.bind('<Return>', lambda e: self.wholesale_price.focus())
        self.wholesale_price.bind('<Return>', lambda e: self.retail_price.focus())
        self.retail_price.bind('<Return>', lambda e: self.base_unit.focus())
        self.base_unit.bind('<Return>', lambda e: self.alt_unit.focus())
        self.alt_unit.bind('<Return>', lambda e: self.unit_ratio.focus())
        self.unit_ratio.bind('<Return>', lambda e: self.description.focus())
        self.description.bind('<Return>', lambda e: self.save_product())
        
    def setup_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Product Information", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Form fields
        fields_frame = ctk.CTkFrame(main_frame)
        fields_frame.pack(fill="x")
        
        # Name
        name_frame = ctk.CTkFrame(fields_frame)
        name_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(name_frame, text="Name*:", font=("Arial", 12), width=120).pack(side="left")
        self.name = ctk.CTkEntry(name_frame, width=350, font=("Arial", 12))
        self.name.pack(side="left", padx=5)
        
        # Wholesale Price
        wholesale_frame = ctk.CTkFrame(fields_frame)
        wholesale_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(wholesale_frame, text="Wholesale Price*:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.wholesale_price = ctk.CTkEntry(wholesale_frame, width=350, font=("Arial", 12))
        self.wholesale_price.pack(side="left", padx=5)
        
        # Retail Price
        retail_frame = ctk.CTkFrame(fields_frame)
        retail_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(retail_frame, text="Retail Price*:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.retail_price = ctk.CTkEntry(retail_frame, width=350, font=("Arial", 12))
        self.retail_price.pack(side="left", padx=5)
        
        # Base Unit
        base_unit_frame = ctk.CTkFrame(fields_frame)
        base_unit_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(base_unit_frame, text="Base Unit*:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.base_unit = ctk.CTkOptionMenu(base_unit_frame, width=350, font=("Arial", 12),
                                         values=["PCS", "KG", "Meter", "Liter", "Box", "Roll"])
        self.base_unit.pack(side="left", padx=5)
        
        # Alternative Unit
        alt_unit_frame = ctk.CTkFrame(fields_frame)
        alt_unit_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(alt_unit_frame, text="Alt. Unit:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.alt_unit = ctk.CTkOptionMenu(alt_unit_frame, width=350, font=("Arial", 12),
                                        values=["PCS", "KG", "Meter", "Liter", "Box", "Roll", "Dozen", "Carton"])
        self.alt_unit.pack(side="left", padx=5)
        
        # Unit Ratio
        ratio_frame = ctk.CTkFrame(fields_frame)
        ratio_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(ratio_frame, text="Unit Ratio:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.unit_ratio = ctk.CTkEntry(ratio_frame, width=350, font=("Arial", 12))
        self.unit_ratio.pack(side="left", padx=5)
        ratio_hint = ctk.CTkLabel(ratio_frame, text="(How many base units in alt. unit)", 
                                font=("Arial", 11), text_color="gray")
        ratio_hint.pack(side="left", padx=5)
        
        # Description
        desc_frame = ctk.CTkFrame(fields_frame)
        desc_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(desc_frame, text="Description:", 
                    font=("Arial", 12), width=120).pack(side="left")
        self.description = ctk.CTkTextbox(desc_frame, width=350, height=100, font=("Arial", 12))
        self.description.pack(side="left", padx=5)
        
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
                                    command=self.save_product)
        self.save_btn.pack(side="left", padx=10)
        
        self.cancel_btn = ctk.CTkButton(button_container, text="Cancel (Esc)", 
                                      font=("Arial", 12),
                                      command=self.destroy)
        self.cancel_btn.pack(side="left", padx=10)
        
        # Set initial focus
        self.name.focus()
        
    def save_product(self):
        name = self.name.get().strip()
        wholesale_price = self.wholesale_price.get().strip()
        retail_price = self.retail_price.get().strip()
        base_unit = self.base_unit.get().strip()
        
        if not all([name, wholesale_price, retail_price, base_unit]):
            messagebox.showerror("Error", "Name, prices, and base unit are required!")
            return
            
        try:
            wholesale_price = float(wholesale_price)
            retail_price = float(retail_price)
            unit_ratio = float(self.unit_ratio.get()) if self.unit_ratio.get().strip() else 1
            
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO products (
                    name, wholesale_price, retail_price, 
                    base_unit, alt_unit, unit_ratio, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                name, wholesale_price, retail_price,
                base_unit, self.alt_unit.get(), unit_ratio,
                self.description.get("1.0", "end-1c")
            ))
            self.db_conn.commit()
            self.callback()  # Refresh the product list
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Prices and unit ratio must be valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {str(e)}")

class ProductMaster(ctk.CTkFrame):
    def __init__(self, parent, db_conn, refresh_callback=None):
        super().__init__(parent)
        self.db_conn = db_conn
        self.refresh_callback = refresh_callback
        self.setup_ui()
        self.setup_bindings()
        
    def setup_bindings(self):
        # Bind keyboard shortcuts to the frame itself
        self.bind('<Control-n>', lambda e: self.show_add_form())
        self.bind('<Control-i>', lambda e: self.import_from_excel())
        self.bind('<Delete>', lambda e: self.delete_product())
        
        # Bind Enter key to search entry
        self.search_entry.bind('<Return>', lambda e: self.on_search())
        
    def setup_ui(self):
        # Title and Add Button Frame
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="Product Management", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(side="left")
        
        # Buttons Frame
        button_frame = ctk.CTkFrame(header_frame)
        button_frame.pack(side="right")
        
        # Add Delete All button
        delete_all_btn = ctk.CTkButton(
            button_frame,
            text="Delete All Products",
            font=("Arial", 12),
            fg_color="red",
            hover_color="darkred",
            command=self.delete_all_products
        )
        delete_all_btn.pack(side="left", padx=5)
        
        # Existing buttons
        import_btn = ctk.CTkButton(button_frame, text="Import Excel (Ctrl+I)", 
                                 font=("Arial", 12),
                                 command=self.import_from_excel)
        import_btn.pack(side="left", padx=5)
        
        add_btn = ctk.CTkButton(button_frame, text="Add New Product (Ctrl+N)", 
                               font=("Arial", 12),
                               command=self.show_add_form)
        add_btn.pack(side="left")
        
        # Search Frame
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Search:", 
                    font=("Arial", 12)).pack(side="left", padx=5)
        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.on_search)
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, 
                                       width=300, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=5)
        
        # Product List Frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Header for product list
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Column headers with widths
        columns = [
            ("ID", 50),
            ("Name", 200),
            ("W.Price", 80),
            ("R.Price", 80),
            ("Base Unit", 80),
            ("Alt Unit", 80),
            ("Ratio", 60),
            ("Description", 200)
        ]
        
        for col, width in columns:
            ctk.CTkLabel(header_frame, text=col, width=width,
                        font=("Arial", 12, "bold")).pack(side="left", padx=2)
        
        # Scrollable frame for product list
        self.product_list = ctk.CTkScrollableFrame(list_frame)
        self.product_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load products
        self.load_products()
        
    def import_from_excel(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select Excel File",
                filetypes=[("Excel files", "*.xlsx *.xls")]
            )
            
            if not file_path:
                return
                
            df = pd.read_excel(file_path)
            required_columns = ['name', 'wholesale_price', 'retail_price', 'base_unit']
            
            # Check if required columns exist
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                messagebox.showerror("Error", 
                    f"Missing required columns: {', '.join(missing_columns)}\n"
                    "Excel file must have columns: name, wholesale_price, retail_price, base_unit"
                )
                return
            
            cursor = self.db_conn.cursor()
            success_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Get values with validation
                    name = str(row['name']).strip()
                    wholesale_price = float(row['wholesale_price'])
                    retail_price = float(row['retail_price'])
                    base_unit = str(row['base_unit']).strip()
                    
                    # Optional fields
                    alt_unit = str(row.get('alt_unit', '')).strip()
                    unit_ratio = float(row.get('unit_ratio', 1))
                    description = str(row.get('description', '')).strip()
                    
                    if not all([name, base_unit]):
                        error_count += 1
                        continue
                        
                    cursor.execute('''
                        INSERT INTO products (
                            name, wholesale_price, retail_price, 
                            base_unit, alt_unit, unit_ratio, description
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        name, wholesale_price, retail_price,
                        base_unit, alt_unit, unit_ratio, description
                    ))
                    success_count += 1
                    
                except (ValueError, KeyError) as e:
                    error_count += 1
                    continue
                    
            self.db_conn.commit()
            self.load_products()
            if self.refresh_callback:
                self.refresh_callback()
                
            messagebox.showinfo("Import Complete", 
                f"Successfully imported {success_count} products.\n"
                f"Failed to import {error_count} products."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Excel file: {str(e)}")
        
    def show_add_form(self):
        def on_product_added():
            self.load_products()
            if self.refresh_callback:
                self.refresh_callback()
                
        AddProductForm(self, self.db_conn, on_product_added)
            
    def delete_product(self):
        # Get the selected product frame
        for child in self.product_list.winfo_children():
            if hasattr(child, 'selected') and child.selected:
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
                    product_id = child.product_id
                    cursor = self.db_conn.cursor()
                    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
                    self.db_conn.commit()
                    self.load_products()
                    if self.refresh_callback:
                        self.refresh_callback()
                break
            
    def delete_all_products(self):
        """Delete all products after confirmation."""
        # Get product count
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM products')
        count = cursor.fetchone()[0]
        
        if count == 0:
            messagebox.showinfo("Info", "No products to delete.")
            return
            
        # Ask for confirmation with product count
        confirm = messagebox.askokcancel(
            "Confirm Delete All",
            f"Are you sure you want to delete all {count} products?\n\n"
            "This action cannot be undone!",
            icon='warning'
        )
        
        if confirm:
            try:
                # Double confirmation for safety
                confirm2 = messagebox.askokcancel(
                    "Final Confirmation",
                    "This will permanently delete ALL products.\n"
                    "Are you absolutely sure?",
                    icon='warning'
                )
                
                if confirm2:
                    cursor.execute('DELETE FROM products')
                    self.db_conn.commit()
                    self.load_products()  # Refresh the list
                    if self.refresh_callback:
                        self.refresh_callback()
                    messagebox.showinfo(
                        "Success", 
                        f"Successfully deleted {count} products."
                    )
                    
            except sqlite3.Error as e:
                messagebox.showerror(
                    "Database Error",
                    f"Failed to delete products: {str(e)}\n\n"
                    "Some products might still exist in the database."
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"An unexpected error occurred: {str(e)}"
                )
            
    def on_search(self, *args):
        search_term = self.search_var.get().lower()
        self.load_products(search_term)
        
    def load_products(self, search_term=''):
        # Clear existing product list
        for widget in self.product_list.winfo_children():
            widget.destroy()
            
        cursor = self.db_conn.cursor()
        if search_term:
            cursor.execute('''
                SELECT * FROM products 
                WHERE lower(name) LIKE ? OR lower(description) LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM products')
            
        for product in cursor.fetchall():
            self.create_product_row(product)
            
    def create_product_row(self, product):
        # Create frame for product row
        row = ctk.CTkFrame(self.product_list)
        row.pack(fill="x", pady=2)
        row.product_id = product[0]  # Store product ID
        row.selected = False  # Track selection state
        
        # Add product details with specific widths
        ctk.CTkLabel(row, text=str(product[0]), width=50).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=product[1], width=200).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=f"₹{product[2]:.2f}", width=80).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=f"₹{product[3]:.2f}", width=80).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=product[4] or "", width=80).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=product[5] or "", width=80).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=str(product[6]) if product[6] else "", width=60).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=product[7] or "", width=200).pack(side="left", padx=2)
        
        # Add selection handling
        def on_click(event):
            # Deselect all other rows
            for child in self.product_list.winfo_children():
                if hasattr(child, 'selected'):
                    child.selected = False
                    child.configure(fg_color=("gray85", "gray25"))
            
            # Select this row
            row.selected = True
            row.configure(fg_color=("gray75", "gray35"))
            
        row.bind('<Button-1>', on_click)
        for widget in row.winfo_children():
            widget.bind('<Button-1>', on_click)
