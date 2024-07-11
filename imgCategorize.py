from textCategortization import find_closest_match
from imgDesc import query
from postRetrieve import fetch_instagram_images
import os

def main(insta_handle):
    # API endpoint construction (you might need to adjust this according to your needs)
    api_endpoint = f"https://api.apify.com/v2/datasets/2ji2YOH9TiQaTvJju/items?token=apify_api_B7DcUY3VZbUhQROKDRT7hv0DDxIqUU31sn6e&directUrls=https://www.instagram.com/{insta_handle}/"
    
    # Step 1: Fetch and download images
    saved_images = fetch_instagram_images(api_endpoint)
    print("Saved images:", saved_images)
    
    # Step 2: Generate descriptions for each image
    descriptions = []
    for image_file in saved_images:
        image_path = os.path.join("images", image_file)  # Ensure the path includes the directory
        json_caption = query(image_path)
        descriptions.append(json_caption[0]['generated_text'])
    
    # Step 3: Combine all descriptions
    combined_descriptions = " ".join(descriptions)
    
    # Step 4: Categorize the combined descriptions
    closest_phrase = find_closest_match(combined_descriptions)
    
    print(f"Combined Descriptions: {combined_descriptions}")
    print(f"Closest Match: {closest_phrase}")

# Usage
if __name__ == "__main__":
    insta_handle = "lillysabri"  # Replace this with the actual Instagram handle
    main(insta_handle)
