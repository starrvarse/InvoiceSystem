# Invoice Management System

The Invoice Management System is a desktop application designed to manage invoices, customers, and products efficiently. It is built using Python and the `customtkinter` library for the user interface.

## Features

- **Invoice Management**: Create, view, and delete invoices.
- **Customer Management**: Add, search, and delete customers.
- **Product Management**: Add, search, and delete products.
- **Import from Excel**: Import product data from Excel files.
- **Generate PDF Invoices**: Generate and save invoices as PDF files.
- **Searchable Combobox**: Modern searchable combobox for easy selection.
- **Keyboard Shortcuts**: Navigate and perform actions using keyboard shortcuts.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/invoice-management-system.git
    cd invoice-management-system
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    python invoice_app.py
    ```

## Usage

- **Invoice Page**: Create new invoices, add items, and generate PDF invoices.
- **Customers Page**: Manage customer information.
- **Products Page**: Manage product information and import from Excel.
- **All Invoices Page**: View and manage all generated invoices.
- **About Page**: View application information and credits.

## Keyboard Shortcuts

- **F1 / Ctrl+I**: Switch to Invoice Page
- **F2 / Ctrl+C**: Switch to Customers Page
- **F3 / Ctrl+P**: Switch to Products Page
- **F4 / Ctrl+L**: Switch to All Invoices Page
- **F5**: Switch to About Page
- **Ctrl+S**: Save invoice
- **Ctrl+A**: Add item to invoice
- **Ctrl+N**: Create new invoice

## Database

The application uses SQLite for data storage. The database file `invoice_system.db` is created automatically in the project directory.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

- **Created by**: Arif Hussain
- **Company**: BigSur Corporation

## Contact

For any inquiries, please contact Arif Hussain at [email@example.com](mailto:contact@bigsur.in).
