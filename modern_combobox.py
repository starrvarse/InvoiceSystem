import customtkinter as ctk
from typing import List, Optional, Callable

class ModernSearchableCombobox(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        # Extract and store values
        self.values = kwargs.pop('values', [])
        self.width = kwargs.pop('width', 200)
        self.font = kwargs.pop('font', ("Arial", 12))
        
        # Create main entry
        self.entry = ctk.CTkEntry(self, width=self.width, font=self.font)
        self.entry.pack(fill="x", expand=True)
        
        # Create dropdown window
        self.dropdown = None
        self.selected_index = -1  # Track currently selected item
        
        # Bind events
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<Down>', self._handle_down)
        self.entry.bind('<Up>', self._handle_up)
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<Escape>', self._hide_dropdown)
        self.entry.bind('<Tab>', lambda e: self._hide_dropdown())
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
    def _show_dropdown(self, event=None):
        if self.dropdown is None:
            # Create new dropdown window
            self.dropdown = ctk.CTkToplevel(self)
            self.dropdown.withdraw()  # Hide initially
            self.dropdown.overrideredirect(True)
            
            # Create listbox
            self.listbox = ctk.CTkScrollableFrame(self.dropdown)
            self.listbox.pack(fill="both", expand=True)
            
            # Position dropdown
            x = self.entry.winfo_rootx()
            y = self.entry.winfo_rooty() + self.entry.winfo_height()
            self.dropdown.geometry(f"{self.width}x200+{x}+{y}")
            
            # Update and show
            self._update_listbox()
            self.dropdown.deiconify()
            self.dropdown.lift()
            
            # Bind listbox events
            self.dropdown.bind('<FocusOut>', self._on_focus_out)
            
    def _hide_dropdown(self, event=None):
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None
            
    def _update_listbox(self):
        if not self.dropdown:
            return
            
        # Clear existing items
        for widget in self.listbox.winfo_children():
            widget.destroy()
            
        # Filter values based on entry text
        search_text = self.entry.get().lower()
        filtered_values = []
        
        # Only filter if there's search text
        if search_text:
            filtered_values = [
                value for value in self.values 
                if search_text in value.lower()
            ]
        else:
            filtered_values = self.values.copy()
        
        # Create frames for each filtered item
        for i, value in enumerate(filtered_values):
            frame = ctk.CTkFrame(self.listbox, fg_color="transparent")
            frame.pack(fill="x", padx=2, pady=1)
            frame.value = value
            
            label = ctk.CTkLabel(
                frame,
                text=value,
                font=self.font,
                anchor="w",
                padx=5
            )
            label.pack(fill="x", expand=True)
            
            # Bind click events
            frame.bind('<Button-1>', lambda e, v=value: self._select_value(v))
            label.bind('<Button-1>', lambda e, v=value: self._select_value(v))
            
            # Bind hover events
            frame.bind('<Enter>', lambda e, f=frame: f.configure(fg_color=("gray75", "gray25")))
            frame.bind('<Leave>', lambda e, f=frame: (
                f.configure(fg_color=("gray75", "gray25")) 
                if self.listbox.winfo_children().index(f) == self.selected_index 
                else f.configure(fg_color="transparent")
             ))
        
        # Update selection index
        if filtered_values:
            self.selected_index = 0
            self._highlight_selected()
        else:
            self.selected_index = -1
            
    def _select_value(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        self._hide_dropdown()
        self.event_generate('<<ComboboxSelected>>')
        
    def _on_key_release(self, event):
        """Handle key release events for searching."""
        if event.keysym not in ('Up', 'Down', 'Return', 'Escape', 'Tab'):
            if not self.dropdown:
                self._show_dropdown(event)
            self._update_listbox()
            
    def _on_enter(self, event):
        if self.dropdown and self.listbox.winfo_children():
            if self.selected_index >= 0:
                self._select_value(self.listbox.winfo_children()[self.selected_index].value)
        return "break"
        
    def _on_focus_out(self, event):
        # Add small delay to allow for click registration
        self.after(100, lambda: self._hide_dropdown() if not (
            self.focus_get() == self.entry or 
            (self.dropdown and self.dropdown.focus_get())
        ) else None)
            
    def _handle_up(self, event=None):
        """Handle up arrow key."""
        if not self.dropdown:
            self._show_dropdown()
            return "break"
            
        items = self.listbox.winfo_children()
        if not items:
            return "break"
            
        self.selected_index = (self.selected_index - 1) % len(items)
        self._highlight_selected()
        return "break"
        
    def _handle_down(self, event=None):
        """Handle down arrow key."""
        if not self.dropdown:
            self._show_dropdown()
            return "break"
            
        items = self.listbox.winfo_children()
        if not items:
            return "break"
            
        self.selected_index = (self.selected_index + 1) % len(items)
        self._highlight_selected()
        return "break"
        
    def _highlight_selected(self):
        """Update the visual selection in the dropdown."""
        items = self.listbox.winfo_children()
        for i, frame in enumerate(items):
            if i == self.selected_index:
                frame.configure(fg_color=("gray75", "gray25"))
            else:
                frame.configure(fg_color="transparent")
            
    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)
        
    def get(self):
        return self.entry.get()
        
    def set_values(self, values):
        self.values = values
        
    def focus(self):
        self.entry.focus()
        
    def configure(self, **kwargs):
        if 'values' in kwargs:
            self.values = kwargs.pop('values')
        super().configure(**kwargs)
        
# Example usage
if __name__ == "__main__": 
    root = ctk.CTk()
    root.geometry("300x200")
    
    def on_select():
        print(f"Selected: {combo.get()}")
    
    combo = ModernSearchableCombobox(
        root,
        width=200,
        values=["Apple", "Banana", "Cherry", "Date", "Elderberry"],
        command=on_select
    )
    combo.pack(padx=20, pady=20)
    
    root.mainloop()
