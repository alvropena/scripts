import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_images(url, folder_name):
    # Create a directory to save images
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Fetch the content from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = urljoin(url, img['src'])  # Get the full URL of the image
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(folder_name, img_url.split(
                '/')[-1])  # Get the image name
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f'Downloaded: {img_name}')
        except Exception as e:
            print(f'Could not download {img_url}. Reason: {e}')


if __name__ == "__main__":
    website_url = input("Enter the URL of the WordPress site: ")
    folder_name = input("Enter the folder name to save images: ")

    if not folder_name:
        print("Error: Folder name cannot be empty.")
    else:
        # Remove leading and trailing slashes
        folder_name = folder_name.strip('/')

        # Use the current working directory as the base
        folder_path = os.path.join(os.getcwd(), folder_name)

        download_images(website_url, folder_path)
