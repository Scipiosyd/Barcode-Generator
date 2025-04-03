import os
from getpass import getpass
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw

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

    # If the text is still there, we can cover it manually with a white rectangle (in case the option doesn't work perfectly)
        width, height = image.size

        crop_height = 80  # You can adjust this value if needed

    # Crop the image to remove the bottom portion (where the text is)
        image_cropped = image.crop((0, 0, width, height - crop_height))

    # Resize to 312x100 pixels
        image_resized = image_cropped.resize((312, 100), Image.LANCZOS)

    # Convert to 8-bit color depth (indexed mode)
        image_8bit = image_resized.convert("P", palette=Image.ADAPTIVE, colors=256)

    # Save the final image as a GIF
        image_8bit.save('barcode_no_text.gif', format='GIF', optimize=True)

        image_cropped.save('barcode_no_text2.gif', format='GIF', optimize=True)


        print(f"Barcode saved successfully as barcode_no_text2.gif")
        os.startfile("barcode_no_text2.gif")
        break;
    else:
        print("The barcode IDs do not match. Please try again.")
    



