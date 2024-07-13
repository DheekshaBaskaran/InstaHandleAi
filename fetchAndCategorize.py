from postRetrieve import fetch_instagram_images
from imgCategorize import categorize


if __name__ == "__main__":
    username = input("Enter the Instagram username to scrape: ")
    saved_images = fetch_instagram_images(username)
    categorize(saved_images)


