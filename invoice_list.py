import customtkinter as ctk
from tkinter import messagebox
import os
import subprocess
import platform
from datetime import datetime
import webbrowser

class InvoiceList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.setup_bindings()
        
    def setup_bindings(self):
        # Bind keyboard shortcuts - only within this frame
        self.bind('<Delete>', lambda e: self.delete_invoice())
        self.bind('<Return>', lambda e: self.print_invoice())
        
    def setup_ui(self):
        # Title Frame
        title_frame = ctk.CTkFrame(self)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(title_frame, text="All Invoices", 
                                 font=("Arial", 16, "bold"))
        title_label.pack(side="left")
        
        # Help label
        help_label = ctk.CTkLabel(title_frame, 
                                text="Select and press Enter to open invoice",
                                font=("Arial", 11),
                                text_color="gray")
        help_label.pack(side="left", padx=20)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(title_frame)
        button_frame.pack(side="right")
        
        self.print_btn = ctk.CTkButton(button_frame, text="Open Invoice (Enter)", 
                                     font=("Arial", 12),
                                     command=self.print_invoice,
                                     state="disabled")
        self.print_btn.pack(side="left", padx=5)
        
        self.delete_btn = ctk.CTkButton(button_frame, text="Delete Invoice (Del)", 
                                      font=("Arial", 12),
                                      command=self.delete_invoice,
                                      state="disabled")
        self.delete_btn.pack(side="left", padx=5)
        
        # Create main list frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Header frame
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        # Column headers with widths
        columns = [
            ("Invoice Number", 200),
            ("Date", 150),
            ("Time", 150),
            ("File Type", 100)
        ]
        
        for col, width in columns:
            ctk.CTkLabel(header_frame, text=col, width=width,
                        font=("Arial", 12, "bold")).pack(side="left", padx=2)
        
        # Scrollable frame for invoice list
        self.invoice_list = ctk.CTkScrollableFrame(list_frame)
        self.invoice_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Load invoices
        self.load_invoices()
        
    def update_button_states(self):
        """Update button states based on selection"""
        has_selection = False
        for child in self.invoice_list.winfo_children():
            if hasattr(child, 'selected') and child.selected:
                has_selection = True
                break
                
        self.print_btn.configure(state="normal" if has_selection else "disabled")
        self.delete_btn.configure(state="normal" if has_selection else "disabled")
        
    def load_invoices(self):
        # Clear existing items
        for widget in self.invoice_list.winfo_children():
            widget.destroy()
            
        # Get list of files in invoices directory
        invoice_dir = "invoices"
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)
            
        # Get all invoices and sort by date (newest first)
        invoices = []
        for filename in os.listdir(invoice_dir):
            if filename.startswith("invoice_"):
                try:
                    # Format: invoice_YYYYMMDD_HHMMSS.pdf
                    date_str = filename.split('_')[1]
                    time_str = filename.split('_')[2].split('.')[0]
                    file_type = filename.split('.')[-1].upper()
                    
                    # Convert to datetime for sorting
                    date_obj = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                    
                    # Format for display
                    display_date = date_obj.strftime("%Y-%m-%d")
                    display_time = date_obj.strftime("%H:%M:%S")
                    
                    invoices.append((date_obj, filename, display_date, display_time, file_type))
                except (IndexError, ValueError):
                    continue
                    
        # Sort invoices by date (newest first)
        invoices.sort(reverse=True)
        
        # Create invoice rows
        for _, filename, display_date, display_time, file_type in invoices:
            self.create_invoice_row(filename, display_date, display_time, file_type)
            
        # Update button states after loading
        self.update_button_states()
        
    def create_invoice_row(self, filename, date, time, file_type):
        # Create frame for invoice row
        row = ctk.CTkFrame(self.invoice_list)
        row.pack(fill="x", pady=2)
        row.filename = filename  # Store filename
        row.selected = False  # Track selection state
        
        # Add invoice details with specific widths
        ctk.CTkLabel(row, text=filename, width=200).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=date, width=150).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=time, width=150).pack(side="left", padx=2)
        ctk.CTkLabel(row, text=file_type, width=100).pack(side="left", padx=2)
        
        # Add selection and double-click handling
        def on_click(event):
            # Deselect all other rows
            for child in self.invoice_list.winfo_children():
                if hasattr(child, 'selected'):
                    child.selected = False
                    child.configure(fg_color=("gray85", "gray25"))
            
            # Select this row
            row.selected = True
            row.configure(fg_color=("gray75", "gray35"))
            
            # Update button states
            self.update_button_states()
            
        def on_double_click(event):
            on_click(event)
            self.print_invoice()
            
        row.bind('<Button-1>', on_click)
        row.bind('<Double-Button-1>', on_double_click)
        for widget in row.winfo_children():
            widget.bind('<Button-1>', on_click)
            widget.bind('<Double-Button-1>', on_double_click)
            
    def delete_invoice(self):
        selected_row = None
        for child in self.invoice_list.winfo_children():
            if hasattr(child, 'selected') and child.selected:
                selected_row = child
                break
                
        if not selected_row:
            messagebox.showwarning("No Selection", 
                                 "Please select an invoice to delete.\n\n" +
                                 "Tip: Click on an invoice in the list to select it.")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this invoice?"):
            filename = selected_row.filename
            filepath = os.path.join("invoices", filename)
            
            try:
                os.remove(filepath)
                selected_row.destroy()
                messagebox.showinfo("Success", "Invoice deleted successfully")
                self.update_button_states()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete invoice: {str(e)}")
                
    def print_invoice(self):
        selected_row = None
        for child in self.invoice_list.winfo_children():
            if hasattr(child, 'selected') and child.selected:
                selected_row = child
                break
                
        if not selected_row:
            messagebox.showwarning("No Selection", 
                                 "Please select an invoice to open.\n\n" +
                                 "Tip: Click on an invoice in the list to select it, " +
                                 "then click 'Open Invoice' or press Enter.")
            return
            
        filename = selected_row.filename
        filepath = os.path.join("invoices", filename)
        
        try:
            # Comprehensive method to open PDF
            if platform.system() == 'Windows':
                # Try multiple methods for Windows
                try:
                    os.startfile(filepath)
                except Exception:
                    try:
                        subprocess.Popen(['start', filepath], shell=True)
                    except Exception:
                        webbrowser.open(filepath)
            elif platform.system() == 'Darwin':  # macOS
                try:
                    subprocess.run(['open', filepath], check=True)
                except subprocess.CalledProcessError:
                    webbrowser.open(filepath)
            else:  # Linux and other systems
                try:
                    subprocess.run(['xdg-open', filepath], check=True)
                except subprocess.CalledProcessError:
                    webbrowser.open(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open invoice: {str(e)}")
            
    def refresh(self):
        """Refresh the invoice list"""
        self.load_invoices()
