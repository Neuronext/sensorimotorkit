import os
from PIL import Image

def resize_images(input_folder, output_folder):
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open an image file
            with Image.open(os.path.join(input_folder, filename)) as img:
                # Get current size
                width, height = img.size
                # Calculate new size
                new_size = (width * 2, height * 2)
                # Resize image
                resized_img = img.resize(new_size, Image.LANCZOS)
                # Save resized image to the output folder
                resized_img.save(os.path.join(output_folder, filename))

if __name__ == "__main__":
    input_folder = 'C:/Users/Data acquisition/Downloads/Ordered Targets/Ordered Targets'  # Change this to your input folder path
    output_folder = 'C:/Users/Data acquisition/sensorimotorkit/assets/Protocol 01 Targets'  # Change this to your output folder path
    resize_images(input_folder, output_folder)

