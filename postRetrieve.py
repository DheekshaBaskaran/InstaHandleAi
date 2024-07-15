import requests
import os
import shutil
from apify_client import ApifyClient


def fetch_instagram_images(username, save_directory="temp/images",
                           apify_token="apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"):
    # Initialize the Apify client
    client = ApifyClient(apify_token)

    # Prepare the input for the Instagram Scraper
    input_params = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsLimit": 5,
        "resultsType": "posts",
    }

    # Run the actor synchronously
    run = client.actor("apify/instagram-scraper").call(run_input=input_params)

    # Fetch the results from the dataset
    dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items

    # Extract display URLs
    display_urls = [item["displayUrl"] for item in dataset_items if "displayUrl" in item]


    # Deleting image folder
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)

    os.makedirs(save_directory)

    # Download each image
    saved_images = []
    for index, url in enumerate(display_urls):
        image_response = requests.get(url)
        image_response.raise_for_status()

        # Save the image
        image_name = f"{username}_{index + 1}.jpg"
        image_path = os.path.join(save_directory, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)
        saved_images.append(image_name)

    return saved_images


# Usage example (to be removed when used as a module)
if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")
    max_images = 5
    saved_images = fetch_instagram_images(username, max_images)
    print("Saved images:", saved_images)