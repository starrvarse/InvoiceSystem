import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, Optional
from customer_master import CustomerMaster
from product_master import ProductMaster
from invoice_list import InvoiceList
from invoice_page import InvoicePage
from database import Database
import sys
import os
from about_page import AboutPage  # Add this import at the top
from PIL import Image  # Add this import at the top with other imports

def setup_customtkinter():
    """Configure customtkinter global settings."""
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Disable automatic DPI scaling
    if sys.platform.startswith('win'):
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

class MainApplication:
    """
    Main application class that manages the invoice system interface.
    Handles page navigation, keyboard shortcuts, and database connections.
    """
    
    def __init__(self) -> None:
        """Initialize the main application."""
        # Create the root window
        self.root = ctk.CTk()
        
        # Configure the window
        self.setup_window()
        
        # Initialize components
        self.initialize_database()
        self.initialize_ui()
        
    def setup_window(self) -> None:
        """Configure the main window settings."""
        self.root.title("Invoice Management System")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"900x700+{x}+{y}")
        
        # Set window icon and logo
        logo_path = os.path.join("assets", "logo.ico")
        
        try:
            # Set window icon
            if os.path.exists(logo_path):
                self.root.iconbitmap(logo_path)
                
                # Create title bar logo
                logo_image = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(24, 24)
                )
                
                # Create title bar with logo
                title_frame = ctk.CTkFrame(self.root, height=30)
                title_frame.pack(fill="x", pady=(0, 5))
                
                # Add logo to title bar
                logo_label = ctk.CTkLabel(
                    title_frame,
                    image=logo_image,
                    text=""
                )
                logo_label.pack(side="left", padx=5)
                
                # Add title text next to logo
                title_label = ctk.CTkLabel(
                    title_frame,
                    text="Invoice Management System",
                    font=("Arial", 14, "bold")
                )
                title_label.pack(side="left", padx=10)
                
        except Exception as e:
            print(f"Failed to load logo: {str(e)}")
            
    def initialize_database(self) -> None:
        """Initialize database connection."""
        try:
            self.db = Database()
            if not self.db.conn:
                messagebox.showerror(
                    "Database Error",
                    "Failed to connect to database.\nPlease ensure the database file exists and is not corrupted."
                )
                self.root.quit()
                return
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Database initialization failed:\n{str(e)}\n\nPlease ensure you have proper permissions."
            )
            self.root.quit()
            return
            
    def initialize_ui(self) -> None:
        """Initialize the user interface."""
        try:
            # Create navigation bar
            self.create_navbar()
            
            # Create main container
            self.main_container = ctk.CTkFrame(self.root)
            self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Initialize pages
            self.pages: Dict[str, ctk.CTkFrame] = {}
            self.create_pages()
            
            # Show initial page
            self.show_page("Invoice")
            
            # Setup keyboard shortcuts
            self.setup_keyboard_shortcuts()
            
            # Bind cleanup on window close
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
        except Exception as e:
            messagebox.showerror(
                "Initialization Error",
                f"Failed to initialize UI:\n{str(e)}\n\nThe application will now close."
            )
            self.root.quit()
        
    def setup_keyboard_shortcuts(self) -> None:
        """Configure keyboard shortcuts for page navigation."""
        shortcuts = {
            '<Control-i>': lambda e: self.show_page("Invoice"),
            '<Control-c>': lambda e: self.show_page("Customers"),
            '<Control-p>': lambda e: self.show_page("Products"),
            '<Control-l>': lambda e: self.show_page("All Invoices"),
            '<F1>': lambda e: self.show_page("Invoice"),
            '<F2>': lambda e: self.show_page("Customers"),
            '<F3>': lambda e: self.show_page("Products"),
            '<F4>': lambda e: self.show_page("All Invoices"),
            '<F5>': lambda e: self.show_page("About")  # Added About shortcut
        }
        
        # Bind shortcuts to root window
        for key, command in shortcuts.items():
            self.root.bind(key, command)
            # Also bind to main container to ensure it works when focus is inside
            self.main_container.bind(key, command)
            
            # Bind to each page
            for page in self.pages.values():
                page.bind(key, command)
        
    def create_navbar(self) -> None:
        """Create the navigation bar with page buttons."""
        # Create navbar frame
        navbar = ctk.CTkFrame(self.root)
        navbar.pack(fill="x", padx=10, pady=5)
        
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        
        # Define navigation buttons (updated)
        nav_items = [
            ("Invoice", "F1"),
            ("Customers", "F2"),
            ("Products", "F3"),
            ("All Invoices", "F4"),
            ("About", "F5")  # Added About page
        ]
        
        # Create navigation buttons
        for name, shortcut in nav_items:
            self.nav_buttons[name] = ctk.CTkButton(
                navbar,
                text=f"{name} ({shortcut})",
                width=150,
                height=35,
                font=("Arial", 12),
                command=lambda n=name: self.show_page(n)
            )
            self.nav_buttons[name].pack(side="left", padx=5)
        
        # Add shortcuts help label
        shortcuts_label = ctk.CTkLabel(
            navbar,
            text="Use F1-F5 or Ctrl+I/C/P/L to switch pages",
            font=("Arial", 11)
        )
        shortcuts_label.pack(side="right", padx=10)
        
        # Add separator
        separator = ctk.CTkFrame(self.root, height=2)
        separator.pack(fill="x", padx=5, pady=5)
        
    def create_pages(self) -> None:
        """Create and initialize all application pages."""
        try:
            # Create invoice page
            self.pages["Invoice"] = InvoicePage(self.main_container, self.db.conn)
            
            # Create customer management page
            self.pages["Customers"] = CustomerMaster(
                self.main_container,
                self.db.conn,
                refresh_callback=self.pages["Invoice"].refresh
            )
            
            # Create product management page
            self.pages["Products"] = ProductMaster(
                self.main_container,
                self.db.conn,
                refresh_callback=self.pages["Invoice"].refresh
            )
            
            # Create invoice list page
            self.pages["All Invoices"] = InvoiceList(self.main_container)
            
            # Add About page
            self.pages["About"] = AboutPage(self.main_container)
            
            # Setup invoice generation callback
            original_generate = self.pages["Invoice"].generate_invoice
            def new_generate():
                result = original_generate()
                if result:  # Only refresh if invoice was generated successfully
                    self.pages["All Invoices"].refresh()
                return result
            self.pages["Invoice"].generate_invoice = new_generate
            
        except Exception as e:
            messagebox.showerror(
                "Initialization Error",
                f"Failed to create application pages:\n{str(e)}\n\nThe application will now close."
            )
            self.root.quit()
        
    def show_page(self, page_name: str) -> None:
        """
        Switch to the specified page and update UI accordingly.
        
        Args:
            page_name: Name of the page to show
        """
        if page_name not in self.pages:
            messagebox.showerror("Error", f"Page '{page_name}' not found")
            return
            
        # Update button states
        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color=("gray70", "gray30"))
        
        # Hide all pages
        for page in self.pages.values():
            page.pack_forget()
        
        # Show selected page
        self.pages[page_name].pack(fill="both", expand=True)
        
        # Set focus and refresh as needed
        self.set_page_focus(page_name)
            
    def set_page_focus(self, page_name: str) -> None:
        """Set focus and perform any necessary updates for the given page."""
        if page_name == "Invoice":
            self.pages[page_name].customer_cb.focus()
        elif page_name in ["Customers", "Products"]:
            if hasattr(self.pages[page_name], 'search_entry'):
                self.pages[page_name].search_entry.focus()
        elif page_name == "All Invoices":
            self.pages[page_name].refresh()
            
    def on_closing(self) -> None:
        """Clean up resources and close the application."""
        try:
            if hasattr(self, 'db'):
                self.db.close()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error during cleanup:\n{str(e)}\n\nSome resources may not have been properly released."
            )
        finally:
            self.root.quit()
            
    def run(self):
        """Start the application main loop."""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror(
                "Fatal Error",
                f"Application encountered an error:\n{str(e)}\n\nPlease contact support if the problem persists."
            )
        finally:
            if hasattr(self, 'db'):
                self.db.close()

def main():
    """Main entry point of the application."""
    try:
        # Configure customtkinter
        setup_customtkinter()
        
        # Create and run application
        app = MainApplication()
        app.run()
        
    except Exception as e:
        messagebox.showerror(
            "Fatal Error",
            f"Application failed to start:\n{str(e)}\n\nPlease contact support if the problem persists."
        )

if __name__ == "__main__":
    main()
