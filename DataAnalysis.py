import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def extract_svg_info(file_path):
    """
    Extracts information from an SVG file.
    """
    info = {
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "creation_date": datetime.fromtimestamp(os.path.getctime(file_path)),
        "modification_date": datetime.fromtimestamp(os.path.getmtime(file_path)),
        "element_counts": {},
        "colors": []
    }

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        for elem in root.iter():
            tag = elem.tag.split('}')[-1]  # Remove namespace if present
            if tag not in info["element_counts"]:
                info["element_counts"][tag] = 0
            info["element_counts"][tag] += 1
            
            # Extract colors
            if 'fill' in elem.attrib:
                info["colors"].append(elem.attrib['fill'])
            if 'stroke' in elem.attrib:
                info["colors"].append(elem.attrib['stroke'])
        
    except ET.ParseError:
        pass  # Handle parse error, possibly log it

    return info

def gather_statistics(directory):
    """
    Gathers statistics for all SVG files in a directory.
    """
    svg_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.svg')]
    data = [extract_svg_info(f) for f in svg_files]

    df = pd.DataFrame(data)
    return df

def display_statistics(df):
    """
    Displays various statistics from the dataframe.
    """
    print("Basic Statistics:")
    print(df.describe(include='all'))

    # Most common elements (shapes)
    element_counts = pd.DataFrame(df['element_counts'].tolist()).sum().sort_values(ascending=False)
    print("\nMost Common Elements:")
    print(element_counts.head(10))
    element_counts.head(10).plot(kind='bar', title='Top 10 Most Common SVG Elements')
    plt.xlabel('Element')
    plt.ylabel('Count')
    plt.show()
    
    # Colors distribution
    all_colors = [color for sublist in df['colors'] for color in sublist]
    color_counts = pd.Series(Counter(all_colors)).sort_values(ascending=False)
    print("\nMost Common Colors:")
    print(color_counts.head(10))
    color_counts.head(10).plot(kind='bar', title='Top 10 Most Common SVG Colors')
    plt.xlabel('Color')
    plt.ylabel('Count')
    plt.show()

# Main Execution
directory = 'D:/DL/svg'  # Replace with your SVG directory path
df = gather_statistics(directory)
display_statistics(df)
