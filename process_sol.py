"""
Author: Nazmus Nasir
Script: Quick H-Alpha Solar Colorizing
Website: https://www.Naztronomy.com
YouTube: https://www.youtube.com/Naztronomy
"""

import cv2
import numpy as np
import os
import sys

def adjust_curve(image_path, red_curve, green_curve, blue_curve, output_path):
    image = cv2.imread(image_path)

    # Split the image into separate color channels
    red_channel = image[:, :, 2]  # OpenCV uses BGR channel order
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 0]

    # Apply the curve adjustments to each color channel
    red_channel_adjusted = apply_curve(red_channel, red_curve)
    green_channel_adjusted = apply_curve(green_channel, green_curve)
    blue_channel_adjusted = apply_curve(blue_channel, blue_curve)

    # Merge the adjusted color channels back into a single image
    adjusted_image = cv2.merge((blue_channel_adjusted, green_channel_adjusted, red_channel_adjusted))

    # Apply unsharp mask
    sharpened_image = apply_unsharp_mask(adjusted_image, amount=4.0, radius=1.0, threshold=7)

    # Save the sharpened image as JPG
    cv2.imwrite(output_path, sharpened_image, [cv2.IMWRITE_JPEG_QUALITY, 100])

def apply_curve(channel, curve):
    lut_in = [0, 127, 255]
    lut_out = curve

    lut_8u = np.interp(np.arange(0, 256), lut_in, lut_out).astype(np.uint8)
    adjusted_channel = cv2.LUT(channel, lut_8u)

    return adjusted_channel

def apply_unsharp_mask(image, amount, radius, threshold):
    blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=radius, sigmaY=radius)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

    return sharpened

# Parse command-line arguments
if len(sys.argv) < 3:
    print("Usage: python script.py -i input_file_or_directory")
    sys.exit(1)

flag = sys.argv[1]
input_path = sys.argv[2]

# Check if the input is a single file or a directory
if flag == "-i" and os.path.isfile(input_path):  # Single file
    red_curve = [0, 255, 255]  # Higher red curve adjustment
    green_curve = [0, 120, 255]  # Lower green curve adjustment
    blue_curve = [0, 20, 255]  # Lower blue curve adjustment

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Get the filename and extension
    file_name, ext = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(output_dir, file_name + "_curved.jpg")

    adjust_curve(input_path, red_curve, green_curve, blue_curve, output_path)
    print(f"Curves and unsharp mask applied to {input_path}. Result saved as {output_path}")
elif flag == "-i" and os.path.isdir(input_path):  # Directory
    # Example usage
    red_curve = [0, 255, 255]  # Higher red curve adjustment
    green_curve = [0, 120, 255]  # Lower green curve adjustment
    blue_curve = [0, 20, 255]  # Lower blue curve adjustment

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each file in the directory
    for file_name in os.listdir(input_path):
        file_path = os.path.join(input_path, file_name)

        # Check if the file is an image
        if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']):
            # Get the filename and extension
            file_name, ext = os.path.splitext(file_name)
            output_path = os.path.join(output_dir, file_name + "_curved.jpg")

            adjust_curve(file_path, red_curve, green_curve, blue_curve, output_path)
            print(f"Curves and unsharp mask applied to {file_path}. Result saved as {output_path}")

    print(f"Curved images saved in the '{output_dir}' directory.")
else:
    print("Invalid flag or input path.")
