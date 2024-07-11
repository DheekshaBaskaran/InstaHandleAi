import requests
import os

def fetch_instagram_images(api_endpoint, save_directory="images"):
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Fetch data from the API
    response = requests.get(api_endpoint)
    response.raise_for_status()  # Ensure the request was successful
    data = response.json()
    
    # Extract display URLs
    display_urls = [item['displayUrl'] for item in data if 'displayUrl' in item]
    
    # Download images and save them locally
    saved_images = []
    for index, url in enumerate(display_urls):
        image_response = requests.get(url)
        image_response.raise_for_status()  # Ensure the image request was successful
        
        # Save the image
        image_name = f"image_{index+1}.jpg"
        image_path = os.path.join(save_directory, image_name)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)
        saved_images.append(image_name)
    
    return saved_images

# Usage example (to be removed when used as a module)
if __name__ == "__main__":
    api_endpoint = "https://api.apify.com/v2/datasets/2ji2YOH9TiQaTvJju/items?token=apify_api_B7DcUY3VZbUhQROKDRT7hv0DDxIqUU31sn6e"
    saved_images = fetch_instagram_images(api_endpoint)
    print("Saved images:", saved_images)
