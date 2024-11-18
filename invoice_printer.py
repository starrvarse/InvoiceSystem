from datetime import datetime
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class InvoicePrinter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
        
    def create_custom_styles(self):
        # Header style - reduced size
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,  # Reduced from 24
            spaceAfter=10,  # Reduced from 30
            alignment=1  # Center alignment
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12
        ))
        
        # Customer info style
        self.styles.add(ParagraphStyle(
            name='CustomerInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            leftIndent=20
        ))
        
    def generate_pdf(self, customer, items, total_amount):
        if not os.path.exists("invoices"):
            os.makedirs("invoices")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"invoices/invoice_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the document content
        story = []
        
        # Add Invoice Title
        story.append(Paragraph("INVOICE", self.styles['CustomTitle']))
        story.append(Spacer(1, 10))  # Reduced spacing
        
        # Add Date
        story.append(Paragraph(
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 20))
        
        # Add Customer Information if available
        if customer:
            story.append(Paragraph("Customer Information:", self.styles['Heading2']))
            story.append(Paragraph(f"Name: {customer[1]}", self.styles['CustomerInfo']))
            story.append(Paragraph(f"Address: {customer[2] or 'N/A'}", self.styles['CustomerInfo']))
            story.append(Paragraph(f"Phone: {customer[3] or 'N/A'}", self.styles['CustomerInfo']))
            if len(customer) > 4:  # Check if email exists in the tuple
                story.append(Paragraph(f"Email: {customer[4] or 'N/A'}", self.styles['CustomerInfo']))
            story.append(Spacer(1, 20))
        
        # Add Items Table
        story.append(Paragraph("Items:", self.styles['Heading2']))
        
        # Create the items table - removed Price Type column
        table_data = [['Product', 'Quantity', 'Unit', 'Total']]  # Header row
        for item in items:
            # item format: (name, quantity, base_unit, price_type, price, total)
            table_data.append([
                item[0],  # Product name
                str(item[1]),  # Quantity
                item[2],  # Base unit
                f"{item[5]:.2f}"  # Total without currency symbol
            ])
            
        # Add total row
        table_data.append(['', '', 'Total:', f"{total_amount:.2f}"])
        
        # Create table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (-2, -1), (-1, -1), colors.black),
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            ('LINEBELOW', (-2, -1), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
        ])
        
        # Create the table and apply the style - adjusted column widths for 4 columns
        table = Table(table_data, colWidths=[3*inch, 1.25*inch, 1*inch, 1.25*inch])
        table.setStyle(table_style)
        story.append(table)
        
        # Add footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Thank you for your business!", self.styles['CustomBody']))
        
        # Build the PDF
        doc.build(story)
        return filename
