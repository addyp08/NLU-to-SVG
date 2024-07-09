import requests
from bs4 import BeautifulSoup
import urllib
import os

# URL of the website to scrape
url = "https://www.svgrepo.com/collection/biological-gene-duotone-icons"

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all <img> tags with class "svg" (assuming the images are stored as SVG)
    images = soup.find_all("img", class_="svg")
    
    # Create a directory to save the images if it doesn't exist
    directory = "downloaded_images"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Download each image
    for i, image in enumerate(images):
        # Get the URL of the image
        image_url = image["src"]
        # Download the image and save it with a unique filename
        filename = os.path.join(directory, f"image_{i}.svg")
        urllib.request.urlretrieve(image_url, filename)
        print(f"Image {i} downloaded successfully.")
else:
    print("Failed to retrieve the webpage.")
