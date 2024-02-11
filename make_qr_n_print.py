import pandas as pd
import qrcode
import re
from create_design import print_ID


# Read Excel data
excel_file = 'Inventory Store Details.xlsx'  # Replace with your actual file path
cols = ['ID', 'Name', 'Quantity', 'Location', 'Category', 'Sub Category']
df = pd.read_excel(excel_file, header=1, names=cols)

# Choose the columns for QR code generation
qr_code_data_columns = ['ID', 'Name', 'Quantity']


# Create QR codes
name_field = 'Name'
for index, row in df.iterrows():

    if pd.isnull(row[name_field]):
        continue
    else: 
        name = row[name_field]

    data = {
        'ID': row['ID'],
        'Name': row['Name'],
        'Quantity': row['Quantity'],
        'Location': row['Location'],
        'Category': row['Category'],
        'Sub Category': row['Sub Category'],
    }

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
 
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save or display the QR code image
    # # Replace invalid characters in the filename
    invalid_chars = r'[\/:*?"<>|]'
    data['Name'] = re.sub(invalid_chars, '_', data['Name'])  # Replace invalid characters in the 'Name' field
    qr_code_file = f"QR_{data['Name']}.png"
 
    img.save(f'qr_image/{qr_code_file}')

    print_ID(data)
    
    
    print(f'QR Code generated and saved as {qr_code_file}\n')