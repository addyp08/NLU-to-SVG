
import cairosvg
from PIL import Image, ImageTk
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
import tkinter as tk
from tkinter import Label, filedialog

# Function to convert SVG to PNG
def convert_svg_to_png(svg_path, png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)

# Function to generate description using Hugging Face model
def generate_description(png_path):
    # Load the pre-trained model and processor from Hugging Face
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Open the image
    image = Image.open(png_path)

    # Process the image and generate the description
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    return description

# Main function to convert SVG to PNG and generate description
def main(svg_path):
    png_path = "temp_image.png"
    
    # Convert SVG to PNG
    convert_svg_to_png(svg_path, png_path)
    
    # Generate description from PNG
    description = generate_description(png_path)
    
    return png_path, description

# Function to handle the button click
def on_button_click():
    # Open file dialog to select an SVG file
    svg_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if svg_path:
        png_path, description = main(svg_path)
        display_result(png_path, description)

# Function to display the SVG image and description in the GUI
def display_result(png_path, description):
    # Load and display the image
    image = Image.open(png_path)
    image = image.resize((300, 300), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)
    image_label.image = image_tk
    
    # Display the description
    description_label.config(text=description)

# Set up the GUI
root = tk.Tk()
root.title("SVG to Description Generator")

# Add a button to select the SVG file
button = tk.Button(root, text="Select SVG File", command=on_button_click)
button.pack()

# Add a label to display the image
image_label = Label(root)
image_label.pack()

# Add a label to display the description
description_label = Label(root, text="", wraplength=300)
description_label.pack()

# Start the GUI event loop
root.mainloop()

