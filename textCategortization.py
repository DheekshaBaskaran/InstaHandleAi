import os
from mistralai.client import MistralClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Set Mistral API key
os.environ["MISTRAL_API_KEY"] = "gTkvXwvzuMY7Rvi92LXGoqqnRK0WVj4u"
api_key = os.environ["MISTRAL_API_KEY"]

# Categories
#categories =  ["Fashion", "Food", "Travel", "Fitness", "Photography", "Art", "Beauty", "Music", "Health", "Nature", "Pets", "Home Decor", "DIY", "Sports", "Books", "Movies", "Gaming", "Technology", "Cars", "Fashion Accessories", "Jewelry", "Architecture", "Design", "Education", "Business", "Finance", "Marketing", "Lifestyle", "Parenting", "Cooking", "Gardening", "Crafts", "Shopping", "Events", "Weddings", "Real Estate", "Travel Destinations", "Hiking", "Yoga", "Sustainability", "Environment", "Politics", "History", "Science", "Motivation", "Inspirational Quotes", "Entrepreneurship", "Influencers", "Celebrities", "Influencer Marketing", "Celebrity News", "Fashion Trends", "Street Style", "Makeup", "Skincare", "Cosmetics", "Hairstyles", "Tattoos", "Piercings", "Dance", "Music Festivals", "Concerts", "Art Exhibitions", "Film Festivals", "Comic Books", "Video Games", "Tech Gadgets", "Virtual Reality", "Automobiles", "Luxury Lifestyle", "Vintage Fashion", "Interior Design", "Home Renovation", "Parenting Tips", "Family Travel", "Healthy Eating", "Nutrition", "Vegan Lifestyle", "Pet Care", "Pet Adoption", "Fashion Design", "Startup Life", "Cryptocurrency", "Personal Finance", "Travel Tips", "Adventure Travel", "Digital Nomads", "Fitness Challenges", "Mental Health Awareness", "Mindfulness", "Environmental Activism", "Social Causes", "Community Building", "Podcasts", "Online Learning", "Remote Work", "Job Hunting", "Digital Marketing", "E-commerce", "Luxury Travel", "Solo Travel", "Group Travel", "Sports Events", "Outdoor Sports", "Extreme Sports", "Healthy Living", "Home Workouts", "Gym Workouts", "Outdoor Adventures", "Local Cuisine", "Cultural Festivals", "Holiday Celebrations", "Fashion Blogging", "Travel Influencers", "Digital Art", "Street Photography", "Adventure Photography", "Product Reviews", "DIY Projects", "Online Classes", "Online Courses", "Learning Languages", "Book Reviews", "Movie Reviews", "Gaming Communities", "Technology Reviews", "Car Reviews", "Luxury Cars", "Fashion Accessories", "Handmade Jewelry", "Urban Architecture", "Minimalist Design", "Green Living", "Parenting Hacks", "Family Activities", "Healthy Recipes", "Fitness Tips", "Gym Motivation", "Inspirational Stories", "Digital Entrepreneurship", "Social Media Marketing", "Celebrity Fashion", "Beauty Tips", "Makeup Tutorials", "Skincare Routines", "Hair Care", "Body Art", "Dance Performances", "Music Concerts", "Art Galleries", "Film Reviews", "Comic Art", "Gamer Lifestyle", "VR Experiences", "Luxury Watches", "Vintage Cars", "Modern Architecture", "Smart Home Technology", "Renovation Projects", "Child Development", "Educational Toys", "Healthy Snacks", "Vegan Recipes", "Pet Training", "Fashion Illustration", "Tech Startups", "Blockchain Technology", "Investment Strategies", "Travel Inspiration", "Adventure Sports", "Remote Working Tips", "Freelance Life", "Job Tips", "SEO Tips", "Online Retail", "Luxury Destinations", "Solo Travel Tips", "Travel Photography", "Action Sports", "Outdoor Exploration", "Farm-to-Table", "Local Culture", "Cultural Diversity", "Holiday Travel", "Fashion Influencers", "Digital Artists", "City Life"]
categories = [ "Fashion", "Food", "Travel", "Fitness", "Photography", "Art", "Beauty", "Music",
    "Health", "Nature", "Pets", "Home Decor", "DIY", "Sports", "Books", "Movies",
    "Gaming", "Technology", "Cars", "Architecture", "Design", "Education", "Business",
    "Finance", "Marketing", "Lifestyle", "Parenting", "Cooking", "Gardening", "Crafts",
    "Shopping", "Events", "Real Estate", "Hiking", "Yoga", "Sustainability", "Environment",
    "Politics", "History", "Science", "Motivation", "Influencers", "Celebrities",
    "Community Building", "Entertainment", "Work", "Reviews", "Family"]



# Model
model = "mistral-embed"

# MistralClient instance with the API key
client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

# Retrieve embeddings for all categories in one call
try:
    response = client.embeddings(model=model, input=categories)
    embeddings = [item.embedding for item in response.data]
    embeddings = np.array(embeddings)
except Exception as e:
    print(f"Error retrieving embeddings: {e}")

def find_closest_match(input_text):
    # Compute embedding for input text
    input_embedding_response = client.embeddings(model=model, input=[input_text])
    try:
        input_embedding = input_embedding_response.data[0].embedding
    except Exception as e:
        print(f"Error retrieving embedding for input text '{input_text}': {e}")
        return None

    # Calculate cosine similarity between input embedding and each category's embedding
    similarities = []
    for category_embedding in embeddings:
        similarity = cosine_similarity([input_embedding], [category_embedding])[0][0]
        similarities.append(similarity)

    # Find the index of the closest match
    closest_index = np.argmax(similarities)
    closest_category = categories[closest_index]

    return closest_category

"""# Usage
input_text = "weights"
closest_category = find_closest_match(input_text)

print(f"Input: {input_text}")
print(f"Closest Match: {closest_category}")"""