import requests
import os
import shutil
from apify_client import ApifyClient
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Set your Apify API token
APIFY_TOKEN = "apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"

# Set your Mistral API key
MISTRAL_API_KEY = "gTkvXwvzuMY7Rvi92LXGoqqnRK0WVj4u"

# Categories for categorization
categories = [
    "Fashion", "Food", "Travel", "Fitness", "Photography", "Art", "Beauty",
    "Music", "Health", "Nature", "Pets", "Home Decor", "DIY", "Sports",
    "Books", "Movies", "Gaming", "Technology", "Cars", "Architecture",
    "Design", "Education", "Business", "Finance", "Marketing", "Lifestyle",
    "Parenting", "Cooking", "Gardening", "Crafts", "Shopping", "Events",
    "Real Estate", "Hiking", "Yoga", "Sustainability", "Environment",
    "Politics", "History", "Science", "Motivation", "Influencers", "Celebrities",
    "Community Building", "Entertainment", "Work", "Reviews", "Family"
]

def fetch_instagram_posts(username, save_directory="temp/images", apify_token=APIFY_TOKEN):
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
    captions = [item.get("caption", "No caption available.") for item in dataset_items]

    # Check if the save directory exists, and delete it if it does (makes sure new pics don't get added along with old ones)
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

    return saved_images, captions  # Return the list of saved images and captions

def user_message(inquiry):
    return f"""
    You are a social media analysis bot. Your task is to assess the content of an Instagram post caption
    and categorize it into one of the following predefined categories:

    {', '.join(categories)}

    If the text doesn't fit into any of the above categories, classify it as:
    Other

    You will only respond with the predefined category. Do not include the word "Category".
    Do not provide explanations or notes. Only return one category and nothing else.

    Inquiry: {inquiry}
    """

def run_mistral(user_message, model="mistral-medium"):
    client = MistralClient(api_key=MISTRAL_API_KEY)
    messages = [ChatMessage(role="user", content=user_message)]
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content

def choose_category(input_text):
    return run_mistral(user_message(input_text))

if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")
    images, captions = fetch_instagram_posts(username)
    caption_categories = [choose_category(caption) for caption in captions]

    for idx, caption in enumerate(captions):
        print(f"Caption {idx + 1}: {caption}\nCategory: {caption_categories[idx]}")
