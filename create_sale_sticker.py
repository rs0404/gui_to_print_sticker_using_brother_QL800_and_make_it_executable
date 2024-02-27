from PIL import Image, ImageDraw, ImageFont
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends.helpers import send
import sys
from brother_ql.conversion import convert
import os


backend = None
model = 'QL-800'
# printer = 'usb://Brother/QL-800?serial=000C3G563318'
printer = 'usb://0x04f9:0x209b'

canvas_width_mm= 62
canvas_height_mm = 70     

outer_rect_coord_in_mm = [59, 65]
inner_rect_coord_in_mm = [57,63]
outer_rect_size = 1    # Size in pixel
inner_rect_size = 2    # Size in pixel

# Declaration of global variable for rectangle coordinates
outer_rect_start_coord_in_pixel = (0,0)
inner_rect_start_coord_in_pixel = (0,0)
outer_rect_end_coord_in_pixel = (0,0)
inner_rect_end_coord_in_pixel = (0,0)


 # Insert yarsa logo and address
yarsa_width = 57    # In mm
yarsa_height = 20   # In mm
yarsa_offset = 2    # Offset value is in mm and is used to align text within the inner rect

data_head = ['Name: ', 'Address: ', 'Phone: ', 'Payment: ']     # Following data to be inserted
head_gap_in_mm = 2


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_path = os.path.abspath(os.path.dirname(__file__))
    
    return os.path.join(base_path, relative_path)


# print("Hello Hello Hello HelloHello HelloHello HelloHello HelloHello Hello")
# print(resource_path("assets/Roboto-Regular.ttf\n\n"))
# # Define fonts
# abs_path = "/Users/spark/Documents/Office/NiziPowerSaleSticker"
data_font_small = ImageFont.truetype(resource_path("assets/Roboto-Regular.ttf"), 25)
data_font_normal = ImageFont.truetype(resource_path("assets/Roboto-Regular.ttf"), 36)
head_font = ImageFont.truetype(resource_path("assets/Roboto-Bold.ttf"), 40)
# data_font_small = ImageFont.truetype(f"{abs_path}/assets/Roboto-Regular.ttf", 25)
# data_font_normal = ImageFont.truetype(f"{abs_path}/assets/Roboto-Regular.ttf", 36)
# head_font = ImageFont.truetype(f"{abs_path}/assets/Roboto-Bold.ttf", 40)


# Calculate pixel from mm
def mm_to_pixel(mm) :
    dpi = 300
    pixel_size = dpi * mm / 25.4
    return pixel_size


# Draw two rectangles
def draw_rectangles(draw_obj):
    global outer_rect_start_coord_in_pixel
    global inner_rect_start_coord_in_pixel 
    global outer_rect_end_coord_in_pixel
    global inner_rect_end_coord_in_pixel
    outer_rect_end_coord_in_pixel = tuple(int(mm_to_pixel(coord+(canv_dim - coord)/2)) for coord,canv_dim in zip(outer_rect_coord_in_mm,[canvas_width_mm, canvas_height_mm]))
    inner_rect_end_coord_in_pixel = tuple(int(mm_to_pixel(coord+(canv_dim - coord)/2)) for coord,canv_dim in zip(inner_rect_coord_in_mm,[canvas_width_mm, canvas_height_mm]))

    outer_rect_start_coord_in_pixel = tuple(int(mm_to_pixel((canv_dim - coord)/2)) for coord,canv_dim in zip(outer_rect_coord_in_mm,[canvas_width_mm, canvas_height_mm]))
    inner_rect_start_coord_in_pixel = tuple(int(mm_to_pixel((canv_dim - coord)/2)) for coord,canv_dim in zip(inner_rect_coord_in_mm,[canvas_width_mm, canvas_height_mm]))
 
    draw_obj.rectangle([outer_rect_start_coord_in_pixel, outer_rect_end_coord_in_pixel], outline="Black", width=outer_rect_size)
    draw_obj.rectangle([inner_rect_start_coord_in_pixel, inner_rect_end_coord_in_pixel], outline="Black", width=inner_rect_size)
    # draw_obj.rectangle([(0,0), (int(mm_to_pixel(canvas_width_mm)),int(mm_to_pixel(canvas_height_mm)))], outline="Black", width=1)


# Insert Yarsa logo and address in canvas
def insert_yarsa_info_in_canvas(canvas):
    yarsa_image = Image.open(resource_path("assets/logo_and_text.png"))
    # yarsa_image = Image.open(f"{abs_path}/assets/logo_and_text.png")
    width, height = yarsa_image.size
    # print(f"Size of the logo: {width}, {height}\n\n")

    yarsa_image = resize_with_aspect_ratio(yarsa_image,int(mm_to_pixel(inner_rect_coord_in_mm[0]))- 2*inner_rect_size)
    width, height = yarsa_image.size
    # print(f"After resiz, Size of the logo: {width}, {height}\n\n")
    
    yarsa_image_pos = tuple((coord + inner_rect_size) for coord in inner_rect_start_coord_in_pixel)
    # print(f"Yarsa Image Position in pixel: ")
    yarsa_width, yarsa_height =  yarsa_image_pos
    # print(f"Width: {yarsa_width}, Height: {yarsa_width}")
    canvas.paste(yarsa_image, yarsa_image_pos)

    return (width, height)  # Return the logo width and height in pixel
    

 # Draw separation line between the image and the data insert field
def draw_sep_line(draw_obj, yarsa_info_height):
    line_st_pos = (
        inner_rect_start_coord_in_pixel[0],
        inner_rect_start_coord_in_pixel[1] + yarsa_info_height
    )
    line_end_pos = (
        inner_rect_start_coord_in_pixel[0]+ int(mm_to_pixel(inner_rect_coord_in_mm[0])),
        inner_rect_start_coord_in_pixel[1]+yarsa_info_height
    )
    draw_obj.line([line_st_pos, line_end_pos], fill="Black", width=inner_rect_size)
    return line_st_pos


# Resize image by preserving the aspect retio of the image
def resize_with_aspect_ratio(image, new_width=None, new_height=None):
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height
    
    if new_width is not None:
        new_height = int(new_width / aspect_ratio)
    elif new_height is not None:
        new_width = int(new_height * aspect_ratio)
    
    return image.resize((new_width, new_height))

# Validator patterns for Name, Address, Phone No and payment
def validators():
    return {
        'name' : r'^[a-zA-Z]+(?:[-\s\'][a-zA-Z]+)*$',
        'phone' : r'^(9\d{9}|0\d{8}})$',
        'addr' : r'^[a-zA-Z0-9\s.,#-]+$',
        'payment' : r'^[a-zA-Z0-9\s.,#-]+$',
    }
        
# Ask user to input Name, Address, Phone No and payment
def ask_info():
    import re           # Import within the function otherwise re won't work
    val_pat = validators()
    print("Welcome to the Brother QL800 system\n")
    name = input("Enter the user name: ", )
    if not re.match(val_pat['name'], name):
        print(f"Invalid input name: {name}")
        return 0
    addr = input("Enter the address: ")
    while not re.match(val_pat['addr'], addr):
        print(f"Invalid input address: {addr}")
        addr = input("Please enter the correct address or type exit: ")
        if addr == 'exit':
            sys.exit()

    phone = input("Enter the phone number: ")
    while not re.match(val_pat['phone'], phone):
        print(f"Invalid input phone number: {phone}")
        phone = input("Please enter the correct phone number or type exit: ")
        if phone == 'exit':
            sys.exit()

    payment = input("Enter the payment method: ")

    print("Please check the inserted details: ")
    print(f"\n\tName: {name}\n\
          Address: {addr}\n\
          Phone Number: {phone}\n\
          Payment Method {payment}\n")

    confirm = input("Do you want to continue printing, \(Y/N\)?")
    if confirm.lower() == 'y':
        return [name, addr, phone, payment]
    else:
        re = input("Do you want to re-enter the data, \(Y/N\)?")
        if re.lower() == 'y':
            ask_info()
        else:
            sys.exit()

    
# Set position for the input data    
def set_positions(data_no, draw_obj, st_cood):
    st_add = (coord + inner_rect_size for coord in st_cood)
    end_add = (coord - inner_rect_size for coord in inner_rect_end_coord_in_pixel)
    st_add = list(st_add)       # Without this, generator type class is generated which can only be accesed through for loop
    end_add = list(end_add)
    width = end_add[0] - st_add[0]
    height = end_add[1] - st_add[1]
    # print(f" The width is {width} and height is {height}\n\n")
    space_for_each_data = height/data_no
    data_pos = []
    _, font_height, _, _ = draw_obj.textbbox((0, 0), text="TEST", font=head_font) # textbbox to get the font size
    gap = (space_for_each_data - font_height) / 2

    for i in range (data_no):
        data_pos.append((st_add[0] + int(mm_to_pixel(head_gap_in_mm)), i*space_for_each_data + st_add[1] + gap - 20))        # Here 5 is hard coded and need to change
    
    return data_pos

def draw_texts(draw_obj, st_cood):
    data_pos = set_positions(len(data_head), draw_obj, st_cood)
    head_text_px_wth = []

    for i, head in zip(range(len(data_head)),data_head):
        draw_obj.text(data_pos[i], head, font=head_font, fill=(0,0,0))
        width = int(draw_obj.textlength(text=head, font=head_font))
        x,y =  data_pos[i]
        x = x + width
        head_text_px_wth.append((x,y))
        # print(f"Width = {width}, x = {x}, and y={y}")
    return head_text_px_wth


# Insert the data 
def insert_data(draw_obj, data, head_text_px_wth):
    for dta, pos in zip(data, head_text_px_wth):
        (coord+inner_rect_size for coord in pos)
        # print(pos)
        # print(f"Data = {dta}")
        draw_obj.text(pos, text=dta, font=data_font_normal, fill=(0,0,0))
   

def print_ID(data):
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True
    # model_id,fota_version,dfota_version,serial,token,imei,mac
    
    # Create canvas
    canvas = Image.new('RGB', (int(mm_to_pixel(canvas_width_mm)), int(mm_to_pixel(canvas_height_mm))), color="white")
    draw_obj = ImageDraw.Draw(canvas)

    # draw_texts(data, draw_obj)
    draw_rectangles(draw_obj)
    _, yarsa_info_height = insert_yarsa_info_in_canvas(canvas)
    
    # Draw separation line between the image and the data insert field
    st_cood = draw_sep_line(draw_obj, yarsa_info_height)
    
    # Draw the headings
    head_text_px_wth = draw_texts(draw_obj, st_cood)

    # data = ask_info()
    # Insert the entered data
    insert_data(draw_obj, data, head_text_px_wth)

    canvas.save(resource_path("assets/Sticker.png"))
    # canvas.save(f"{abs_path}/assets/Sticker.png")

    printable_canvas = Image.open(resource_path("assets/Sticker.png"))
    # printable_canvas = Image.open(f"{abs_path}/assets/Sticker.png")

    # Create the label
    create_label(qlr, printable_canvas, '62', cut=True, dither=True, threshold=40, compress=True, red=False)
    send(instructions=qlr.data, printer_identifier=printer, backend_identifier=backend, blocking=True)

