import os
from PIL import Image
import numpy as np

def noise_add(image_array):
    # Add more noise by increasing the standard deviation
    # Generate noise based on the shape of the image
    increased_noise = np.random.normal(loc=0, scale=200, size=(image_array.shape[0], image_array.shape[1])).clip(0, 255)
    
    # Add noise to the grayscale image by stacking the noise across three channels for RGB
    noisy_image = image_array + increased_noise

    # Clip values to ensure valid pixel range (0-255) and convert back to an image
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    # Convert the noisy image back to a PIL image
    noisy_image_pil = Image.fromarray(noisy_image)

    return noisy_image_pil

img_dir = "C:/Users/trand/CS 274E/final_project/Lung-PET-CT-img"
dst_dir = "C:/Users/trand/CS 274E/final_project/Lung-PET-CT-img-noise"
os.makedirs(dst_dir, exist_ok=True)

img_list = os.listdir(img_dir)

for image_file in img_list:
    try:
        image_path = os.path.join(img_dir, image_file)
        print(image_path)
        #print(image_path)
        # Open the image in grayscale mode ('L') and convert to a NumPy array
        image = Image.open(image_path).convert("L")
        img_array = np.array(image)
        #print(img_array)

        # Add noise to the image
        noisy_image_pil = noise_add(img_array)
        
        # Save the noisy image to the destination directory
        output_path = os.path.join(dst_dir, f"noisy_{image_file}")
        #print(output_path)
        noisy_image_pil.save(output_path)

        print(f"Saved noisy image to: {output_path}")
    except Exception as e:
        # Log the error and continue with the next file
        print(f"Error processing file {image}: {e}")

