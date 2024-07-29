
from postRetrieve import fetch_instagram_images  # Function to fetch images from an Instagram user's posts
from imgCategorize import categorize  # Function to categorize the saved images


if __name__ == "__main__":

    username = input("Enter the Instagram username to scrape: ")

    # Fetch images from the specified Instagram user's posts
    saved_images = fetch_instagram_images(username)

    # Categorize the fetched images using the categorize function
    categorize(saved_images)

