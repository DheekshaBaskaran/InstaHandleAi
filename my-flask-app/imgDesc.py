# Importing the requests library to make HTTP requests
import requests

# API endpoint for the Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"

# Authorization header with  API key
headers = {
    "Authorization": "Bearer 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"
}


def query(filename):
    # Open the specified image file in binary read mode
    with open(filename, "rb") as f:
        data = f.read()  # Read the image data

   #sending a request to API to analyze the image data provided.
    response = requests.post(API_URL, headers=headers, data=data)

    # Return the JSON response from  API
    return response.json()


