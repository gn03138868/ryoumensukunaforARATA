#Sugi for A4 sample images

from PIL import Image
import os

# input path
input_image_path = r"X:\XX\XXX\XXXX.jpg"
## rewrite the image name you wish to input in A4 size

# output path
output_folder = r"Y:\YY\YYY\YYYY"
## rewrite the output folder name you with for the cut 400X400 pixel images

# crop size definition
crop_size = (400, 400)

def crop_image(image_path, output_folder, crop_size):
    # Open an image file
    with Image.open(image_path) as img:
        img = img.convert('RGB')  # Convert the image to RGB mode
        original_dpi = img.info.get('dpi', (600, 600))  # Default to 600 DPI if not specified
        print(f"Original image DPI: {original_dpi}")
        
        # Image width and height
        img_width, img_height = img.size
        if isinstance(crop_size, int):
            crop_width = crop_height = crop_size
        elif isinstance(crop_size, tuple) and len(crop_size) == 2:
            crop_width, crop_height = crop_size
        else:
            raise ValueError("crop_size should be an int or a tuple of two ints")
        
        # Calculate the number of crops in both directions
        crops_w = img_width // crop_width
        crops_h = img_height // crop_height
        count = 0
        for i in range(crops_h):
            for j in range(crops_w):
                left = j * crop_width
                top = i * crop_height
                right = left + crop_width
                bottom = top + crop_height
                
                # Crop the image
                cropped_img = img.crop((left, top, right, bottom))
                # Save the cropped image with original DPI
                output_path = os.path.join(output_folder, f"0008_20230209T141033_W_weakzone_WB_{left}_{top}_{right}_{bottom}_{count}_arata.jpg")
                cropped_img.save(output_path, dpi=original_dpi, quality=100)
                
                # Verify DPI of saved image
                with Image.open(output_path) as saved_img:
                    saved_dpi = saved_img.info.get('dpi', (0, 0))
                    print(f"Saved image DPI: {saved_dpi}")
                    if saved_dpi != original_dpi:
                        print(f"Warning: DPI mismatch for {output_path}")
                
                count += 1


crop_image(input_image_path, output_folder, crop_size)
