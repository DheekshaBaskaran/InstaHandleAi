import requests
import os
import shutil
from apify_client import ApifyClient
def fetch_instagram_images(username, save_directory="temp/images",
                           apify_token="apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"):

    client = ApifyClient(apify_token)

    # Prepare the input parameters for the Instagram Scraper
    input_params = {
        "directUrls": [f"https://www.instagram.com/{username}/"],  # URL of the Instagram profile
        "resultsLimit": 5,  # Limit the number of posts to scrape
        "resultsType": "posts",  # Specify that we want posts
    }

    # Run Apify actor
    run = client.actor("apify/instagram-scraper").call(run_input=input_params)

    dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

    # Extract the display URLs of the images from the dataset items
    display_urls = [item["displayUrl"] for item in dataset_items if "displayUrl" in item]

    # Check if the save directory exists, and delete it if it does (makes sure new pics dont get added along w old ones)
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)  # Remove the existing directory and its contents

    # Create a new directory to save the images
    os.makedirs(save_directory)

    # Initialize a list to keep track of saved image names
    saved_images = []
    # Loop through each image URL to download the images
    for index, url in enumerate(display_urls):
        image_response = requests.get(url)
        image_response.raise_for_status()

        # Construct the image name and path for saving
        image_name = f"{username}_{index + 1}.jpg"
        image_path = os.path.join(save_directory, image_name)  # Full path to save the image


        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)  # Write the image content to the file
        saved_images.append(image_name)  # Add the saved image name to the list

    return saved_images  # Return the list of saved images

"""# Usage 
if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")  # Prompt user for the Instagram username
    max_images = 5  # Set a maximum number of images to scrape
    saved_images = fetch_instagram_images(username, max_images)  # Call the function to fetch images
    print("Saved images:", saved_images)  # Print the names of the saved images"""
