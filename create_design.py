from PIL import Image, ImageDraw, ImageFont
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends.helpers import send
from barcode import Code128
import io

from brother_ql.conversion import convert

backend = None
model = 'QL-800'
# printer = 'usb://Brother/QL-800?serial=000C3G563318'
printer = 'usb://0x04f9:0x209b'

canvas_width= 310
canvas_height = 200

qr_size = 100
yarsa_logo_size = 40
texts_offset = 3
qr_location = (canvas_width - (qr_size + 1),yarsa_logo_size + texts_offset)
yarsa_logo_location = (int((canvas_width - yarsa_logo_size)/2 - 10), texts_offset)
yarsa_tech_font_size = 20
text_font_size = 15


font_small = ImageFont.truetype("./assets/Roboto-Regular.ttf", text_font_size)
font_bold = ImageFont.truetype("./assets/Roboto-Bold.ttf", text_font_size)
font_roboto_yarsa = ImageFont.truetype("./assets/Roboto-Bold.ttf", yarsa_tech_font_size)


# Resize image by preserving the aspect retio of the image
def resize_with_aspect_ratio(image, new_height=None, new_width=None):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    
    if new_width is not None:
        new_height = int(new_width / aspect_ratio)
    elif new_height is not None:
        new_width = int(new_height * aspect_ratio)
    
    return image.resize((new_width, new_height))

def draw_texts(data, draw_obj):
    y_positionTrack = 1
    x_positionOffset = 4
    y_positionOffset = yarsa_logo_size + 10
    line_gap_size = text_font_size + texts_offset
    texts = [
        {"text": "ID: ", "font": font_bold, "inline": data['ID'], "inline_font": font_small},
        {"text": "Comp Name : ", "font": font_bold, "inline": data['Name'], "inline_font": font_small},
        {"text": "Qty : ", "font": font_bold, "inline": data['Quantity'], "inline_font": font_small},
        {"text": "Cat : ", "font": font_bold, "inline": data['Category'], "inline_font": font_small},
        {"text": "Sub-Cat: ", "font": font_bold, "inline": data['Sub Category'], "inline_font": font_small},
        # {"text": "Description : ", "font": font_bold, "inline": data['Description'], "inline_font": font_small},
    ]

    for i, text_entry in enumerate(texts):  # enumerate make i initial value 0
        text_entry['pos'] = text_entry['pos'] = (x_positionOffset, y_positionTrack + y_positionOffset + i * line_gap_size)

    for i, text_entry in enumerate(texts):  
        x, y = text_entry['pos']  # Extract position from the entry
        draw_obj.text((x, y), text_entry['text'], font=text_entry['font'], fill=(0, 0, 0))  # Draw the main text
        
        a =  draw_obj.textlength(text_entry['text'], font=text_entry['font'])
        # print(a)
        # print("\n\n")

        x = int(a) + x
        # print(f"x = {text_width}\n")
        if text_entry['inline']:  # Check if there's inline content
            inline_text = f"{text_entry['inline']}"  # Convert inline content to string
            draw_obj.text((x, y), inline_text, font=text_entry['inline_font'], fill=(0, 0, 0))  # Draw inline content

    # draw_obj.text((int(canvas_width/2 + yarsa_logo_size + 10), texts_offset), "Yarsa Tech", font=font_roboto_yarsa, fill=(0, 0, 0))


def insert_pixels(draw_obj):
    for i in range(0,canvas_width, 20):
        draw_obj.text((i,180), f"{i}", font=font_small, fill=(0,0,0))


def print_ID(data):
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True
    # model_id,fota_version,dfota_version,serial,token,imei,mac
    
    # Create canvas
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=(255, 255, 255))

    qr_code_file = f"QR_{data['Name']}.png"

    # Open and resize QR and logo image and resize it
    qr_image = Image.open(f'qr_image/{qr_code_file}', 'r')
    qr_image = resize_with_aspect_ratio(qr_image, qr_size)
    logo_image = Image.open(f"assets/yarsa_logo.png")
    logo_image = resize_with_aspect_ratio(logo_image, yarsa_logo_size)

    # Print in canvas
    canvas.paste(qr_image, qr_location)
    canvas.paste(logo_image, yarsa_logo_location)

    # Insert text
    # Define the text content and positions
    
    draw_obj = ImageDraw.Draw(canvas)
    # Draw outline rectangle
    # draw_obj.rectangle([(0,0), (canvas_width-1, canvas_height-1)], outline="Black")
    
    # insert_pixels(draw_obj)
    draw_texts(data, draw_obj)
    
    canvas.save(f'assets/{qr_code_file}')

    printable_canvas = Image.open(f'assets/{qr_code_file}')
    # Create the label
    create_label(qlr, printable_canvas, '62', cut=True, dither=True, threshold=40, compress=True, red=False)

    # for i in range(1):
    send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)