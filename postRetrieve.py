import requests
import os
from apify_client import ApifyClient
import openai

# Apify API token
APIFY_TOKEN = "apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"

# OpenAI API key
OPENAI_API_KEY = os.getenv('api_key')

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

    return [], captions  # Return an empty list for saved images and the captions

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