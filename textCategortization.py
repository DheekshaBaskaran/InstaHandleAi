import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Set Mistral API key
api_key = "gTkvXwvzuMY7Rvi92LXGoqqnRK0WVj4u"

# Categories
categories = ["Fashion", "Food", "Travel", "Fitness", "Photography", "Art", "Beauty", "Music",
    "Health", "Nature", "Pets", "Home Decor", "DIY", "Sports", "Books", "Movies",
    "Gaming", "Technology", "Cars", "Architecture", "Design", "Education", "Business",
    "Finance", "Marketing", "Lifestyle", "Parenting", "Cooking", "Gardening", "Crafts",
    "Shopping", "Events", "Real Estate", "Hiking", "Yoga", "Sustainability", "Environment",
    "Politics", "History", "Science", "Motivation", "Influencers", "Celebrities",
    "Community Building", "Entertainment", "Work", "Reviews", "Family"]

def user_message(inquiry):
    user_message = (
        f"""
        You are a social media analysis bot. Your task is to assess the content of an Instagram post 
        and categorize it after <<<>>> into one of the following predefined categories:
        
        {', '.join(categories)}
        
        If the text doesn't fit into any of the above categories, classify it as:
        Other
        
        You will only respond with the predefined category. Do not include the word "Category". Do not provide explanations or NOTES. Only return one category and nothing else.
        
        ####
        Here are some examples:
        
        Inquiry: Man in gym with a barbell and a weight machine flexing in the mirror
        Category: Fitness
        Inquiry: Woman showing a picture of her food on a plate
        Category: Food 
        Inquiry: A group of paintings on the wall in a museum
        Category: Art
        ###
    
        <<<
        Inquiry: {inquiry}
        >>>
        """
    )
    return user_message

def run_mistral(user_message, model="mistral-medium"):
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="user", content=user_message)
    ]
    chat_response = client.chat(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content

def chooseCategory(input_text):
    return run_mistral(user_message(input_text))