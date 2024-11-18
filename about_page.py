
import customtkinter as ctk
from PIL import Image
import os

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Try to load and display logo
        try:
            logo_path = os.path.join("assets", "logo.ico")
            if os.path.exists(logo_path):
                logo_image = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(128, 128)
                )
                logo_label = ctk.CTkLabel(
                    main_frame,
                    image=logo_image,
                    text=""
                )
                logo_label.pack(pady=(20, 30))
        except Exception as e:
            print(f"Failed to load logo: {str(e)}")
        
        # App title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Invoice Management System",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Version info
        version_label = ctk.CTkLabel(
            main_frame,
            text="Version 1.0.0",
            font=("Arial", 14)
        )
        version_label.pack(pady=(0, 30))
        
        # Creator info
        creator_label = ctk.CTkLabel(
            main_frame,
            text="Created by Arif Hussain",
            font=("Arial", 16, "bold")
        )
        creator_label.pack(pady=(0, 10))
        
        # Company info
        company_label = ctk.CTkLabel(
            main_frame,
            text="Founder of BigSur Corporation",
            font=("Arial", 14)
        )
        company_label.pack(pady=(0, 30))
        
        # Copyright notice
        copyright_label = ctk.CTkLabel(
            main_frame,
            text="© 2024 BigSur Corporation. All rights reserved.",
            font=("Arial", 12),
            text_color="gray"
        )
        copyright_label.pack(pady=(20, 0))