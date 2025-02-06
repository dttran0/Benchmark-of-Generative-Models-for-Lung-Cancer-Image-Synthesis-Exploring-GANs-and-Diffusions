import os 
import pydicom
import numpy as np
from PIL import Image
import SimpleITK as sitk
import cv2

def convert_dcm_to_image(input_folder, output_folder, image_format="png"):
    """
    Convert all DICOM (.dcm) files in a folder to PNG or JPG.
    
    Args:
        input_folder (str): Path to the folder containing DICOM files.
        output_folder (str): Path to save the converted images.
        image_format (str): Desired output image format ("png" or "jpg").
    """
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    counter = 1
    for root, _, files in os.walk(input_folder):
        for file in files:
            print(file)
            if file.endswith(('.dcm', '.zraw')):
                file_path = os.path.join(root, file)
                # Read DICOM file
                dicom = pydicom.dcmread(file_path)
                # Extract pixel data and normalize
                pixel_array = dicom.pixel_array
                normalized = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array)) * 255
                normalized = normalized.astype(np.uint8)
                # Convert to PIL Image
                image = Image.fromarray(normalized)
                # Save as PNG or JPG
                output_filename = f"image_{counter}.{image_format}"
                output_path = os.path.join(output_folder, output_filename)
                image.save(output_path)
                #print(f"Converted: {file_path} -> {output_path}")


def convert_mhd_to_image(input_folder, output_folder, image_format="png"):
    """
    Convert all MHD (.mhd) files and associated ZRAW (.zraw) in a folder to PNG or JPG slices.
    
    Args:
        input_folder (str): Path to the folder containing MHD and ZRAW files.
        output_folder (str): Path to save the converted image slices.
        image_format (str): Desired output image format ("png" or "jpg").
    """
    #print(os.listdir(input_folder))
    files = [f for f in os.listdir(input_folder) if f.endswith('.mhd')]
    #print(files)
    for file in files:
    # Load the MHD file
        file_path = os.path.join(input_folder, file)
        itk_image = sitk.ReadImage(file_path)
        image_array = sitk.GetArrayFromImage(itk_image)  # Shape: (slices, height, width)
        
        # Normalize pixel values (optional, depending on the task)
        min_val, max_val = np.min(image_array), np.max(image_array)
        image_array = ((image_array - min_val) / (max_val - min_val) * 255).astype(np.uint8)

        # Save each slice as a PNG file
        for i, slice_img in enumerate(image_array):
            slice_name = f"{file.split('.')[0]}_slice_{i:04d}.png"
            output_path = os.path.join(output_folder, slice_name)
            
            # Save using OpenCV
            cv2.imwrite(output_path, slice_img)
# Example usage
input_dir = "./lung data/LUNA16/seg-lungs-LUNA16/seg-lungs-LUNA16"  # Replace with your input folder path
output_dir = "./LUNA16-2"  # Replace with your desired output folder
os.makedirs(output_dir, exist_ok=True)
convert_mhd_to_image(input_dir, output_dir, image_format="png")

# for root, _, files in os.walk(input_dir):
#     for f in files:
#         input_path = os.path.join(root, f)
        
#         # Modify the output file name to have a .png extension
#         output_filename = os.path.splitext(f)[0] + ".png"
#         output_path = os.path.join(output_dir, output_filename)
        
#         try:
#             # Open and save the image in PNG format
#             with Image.open(input_path) as image:
#                 # Convert to RGB mode if necessary (e.g., for grayscale or palette images)
#                 if image.mode != "RGB":
#                     image = image.convert("RGB")
#                 image.save(output_path, format="PNG")
#             print(f"Saved as PNG: {output_path}")
#         except Exception as e:
#             print(f"Failed to process {f}: {e}")
# convert_dcm_to_image(input_dir, output_dir, image_format="png")

#print(len(os.listdir("./Lung-PET-CT-img")))