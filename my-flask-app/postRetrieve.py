import os
from apify_client import ApifyClient
import openai

# Set your Apify and OpenAI API keys
APIFY_TOKEN = "apify_api_9s3GF9roqPDUGWx6xhVc1V4skwzSSr4yVKJ6"
OPENAI_API_KEY = os.getenv('api_key')

# Define the list of categories for classification
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

# Fetch Instagram posts for a given username
def fetch_instagram_posts(username, save_directory="temp/images", apify_token=APIFY_TOKEN):
    client = ApifyClient(apify_token)
    input_params = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsLimit": 5,
        "resultsType": "posts",
    }
    run = client.actor("apify/instagram-scraper").call(run_input=input_params)
    dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
    display_urls = [item["displayUrl"] for item in dataset_items if "displayUrl" in item]
    captions = [item.get("caption", "No caption available.") for item in dataset_items]
    return [], captions

# Generate the user message for OpenAI
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

# Run the OpenAI model with the given message
def run_openai(user_message, model="gpt-4o-mini"):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Choose a category for the given input text
def choose_category(input_text):
    return run_openai(user_message(input_text))

# Determine the gender for the given input text
def determine_gender(input_text):
    result = run_openai(user_message(input_text, for_gender=True))
    if result in ["Male", "Female"]:
        return result
    else:
        return "Other"

# Determine the location for the given input text
def determine_location(input_text):
    result = run_openai(user_message(input_text, for_location=True))
    return result if result else "Unknown"
