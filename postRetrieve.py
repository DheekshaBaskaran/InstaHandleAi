import requests
import os
import shutil
from apify_client import ApifyClient
import openai

# Apify API token
APIFY_TOKEN = "apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"

# OpenAI API key
OPENAI_API_KEY = "sk-proj-1yjj1KDzDA3Z71HWrQG5T3BlbkFJaIiO46kL1oNV7kOmkdjt"


# Categories for categorization
categories = [
    "Fashion", "Food", "Travel", "Fitness", "Photography", "Art", "Beauty",
    "Music", "Health", "Nature", "Pets", "Home Decor", "DIY", "Sports",
    "Books", "Movies", "Gaming", "Technology", "Cars", "Architecture",
    "Design", "Education", "Business", "Finance", "Marketing", "Lifestyle",
    "Parenting", "Cooking", "Gardening", "Crafts", "Shopping", "Events",
    "Real Estate", "Hiking", "Yoga", "Sustainability", "Environment",
    "Politics", "History", "Science", "Motivation", "Celebrities",
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


def user_message(inquiry, for_gender=False, for_location=False):
    if for_gender:
        return f"""
        You are a social media analysis bot. Your task is to assess the content of an Instagram post caption
        and determine the likely gender of the person based on the content. Only respond with "Male" or "Female".

        Inquiry: {inquiry}
        """
    elif for_location:
        return f"""
        You are a social media analysis bot. Your task is to assess the content of an Instagram post caption
        and determine the likely location of the person based on the content. Only respond with the location name.

        Inquiry: {inquiry}
        """
    else:
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


def run_openai(user_message, model="gpt-4o-mini"):
    """
    Runs the OpenAI chat completion model with the provided user message and model.

    Parameters:
    - user_message (str): The message to be processed by the OpenAI.
    - model (str): The model to be used for the chat completion (default is "gpt-4").

    Returns:
    - str: The content of the chat response.
    """
    openai.api_key = OPENAI_API_KEY  # Set the OpenAI API key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content'].strip()


def choose_category(input_text):
    """
    Chooses a category for the given input text by running the OpenAI model.

    Parameters:
    - input_text (str): The input text to be categorized.

    Returns:
    - str: The chosen category for the input text.
    """
    return run_openai(user_message(input_text))


def determine_gender(input_text):
    """
    Determines the gender for the given input text by running the OpenAI model.

    Parameters:
    - input_text (str): The input text to determine gender.

    Returns:
    - str: The determined gender for the input text, or "Other" if no gender is determined.
    """
    result = run_openai(user_message(input_text, for_gender=True))
    # Validate and return the gender or "Other" if the result is not valid
    if result in ["Male", "Female"]:
        return result
    else:
        return "Other"
def determine_location(input_text):
    """
    Determines the location for the given input text by running the OpenAI model.

    Parameters:
    - input_text (str): The input text to determine location.

    Returns:
    - str: The determined location for the input text, or "Unknown" if no location is determined.
    """
    result = run_openai(user_message(input_text, for_location=True))
    # Return the result or "Unknown" if the location is not determined
    return result if result else "Unknown"

if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")  # Prompt the user to enter the Instagram username
    images, captions = fetch_instagram_posts(username)  # Fetch the Instagram posts (images and captions) for the given username

    # Aggregate all captions into one text
    aggregated_captions = " ".join(captions)

    # Get a single category for the aggregated captions
    category = choose_category(aggregated_captions)

    # Determine gender from the aggregated captions
    gender = determine_gender(aggregated_captions)

    # Print the aggregated captions, the chosen category, and the determined gender
    print(f"Aggregated Captions: {aggregated_captions}\nCategory: {category}\nGender: {gender}")
