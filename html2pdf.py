import os
import pdfkit

# Directory containing HTML files
html_dir = 'F:/LLM Projects/aiplanet_rag/corpus'
pdf_dir = 'F:/LLM Projects/aiplanet_rag/pdfs'

# Ensure the output directory exists
if not os.path.exists(pdf_dir):
    os.makedirs(pdf_dir)

# Path to wkhtmltopdf executable
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Set options for the PDF generation
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': 'UTF-8',
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'no-outline': None
}

# Function to add UTF-8 meta tag and style if not present
def ensure_utf8_meta_and_style(html_content):
    meta_tag = '<meta charset="UTF-8">'
    style_tag = """
    <style>
        body {
            font-family: Arial, sans-serif;
        }
    </style>
    """
    if meta_tag not in html_content:
        head_end_index = html_content.find('</head>')
        if head_end_index != -1:
            html_content = html_content[:head_end_index] + meta_tag + html_content[head_end_index:]
    
    if style_tag not in html_content:
        head_end_index = html_content.find('</head>')
        if head_end_index != -1:
            html_content = html_content[:head_end_index] + style_tag + html_content[head_end_index:]

    return html_content

# Process each HTML file in the directory
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        html_path = os.path.join(html_dir, filename)
        
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Ensure the HTML file has UTF-8 meta tag and style tag
        updated_html_content = ensure_utf8_meta_and_style(html_content)
        
        # Write the updated HTML content back to the file
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(updated_html_content)
        
        # Convert the updated HTML file to PDF
        pdf_path = os.path.join(pdf_dir, filename.replace('.html', '.pdf'))
        pdfkit.from_file(html_path, pdf_path, configuration=config, options=options)

print("Conversion completed.")
