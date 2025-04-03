import os
from getpass import getpass
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageOps

# Function to resize the image while maintaining aspect ratio and padding to fit the desired label size
def resize_with_padding(image, target_width, target_height):
    # Get original image dimensions
    width, height = image.size
    
    # Calculate aspect ratio
    aspect_ratio = width / height
    
    # Calculate new dimensions that fit within the target size while maintaining aspect ratio
    if aspect_ratio > 1:  # Wider than tall
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:  # Taller than wide
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    
    # Resize image
    image_resized = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Create a new image with target size and a white background
    new_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))
    
    # Calculate position to center the resized image
    left = (target_width - new_width) // 2
    top = (target_height - new_height) // 2
    
    # Paste the resized image onto the new image (with padding)
    new_image.paste(image_resized, (left, top))
    
    return new_image

# Prompt user for barcode ID with hidden input
while True:
    
    barcode_id = getpass("Enter barcode ID: ")  # Barcode ID input will be hidden

    barcode_id2 = getpass("Please enter again to check: ")

    if barcode_id == barcode_id2:
        # Create the barcode for the 'code128' format
        BarcodeClass = barcode.get_barcode_class('code128')
        writer = ImageWriter()

        # Set options to hide the text under the barcode
        writer.set_options({'text': False})  # Disable text below the barcode

        # Create the barcode with the writer
        code = BarcodeClass(barcode_id, writer=writer)

        # Save the barcode as an image (it will create a .png by default)
        filename = code.save('barcode')  # This saves it as 'barcode.png'

        # Open the generated image with Pillow (without appending '.png')
        image = Image.open(filename)  # Open the saved image without adding another .png

        # Get the dimensions of the image
        width, height = image.size

        crop_height = 80  # Adjust this value to remove the text portion

        # Crop the image to remove the bottom portion (where the text is)
        image_cropped = image.crop((0, 0, width, height - crop_height))

        # Resize the image with padding to fit exactly 312x100 while preserving the aspect ratio
        image_resized = resize_with_padding(image_cropped, 312, 100)

        # Convert to 8-bit color depth (indexed mode)
        image_8bit = image_resized.convert("P", palette=Image.ADAPTIVE, colors=256)

        # Save the final image as a GIF
        image_8bit.save('barcode_no_text.gif', format='GIF', optimize=True)

        print(f"Barcode saved successfully as barcode_no_text.gif")
        os.startfile("barcode_no_text.gif")
        break;
    else:
        print("The barcode IDs do not match. Please try again.")
