import os
from mistralai.client import MistralClient
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Set Mistral API key
os.environ["MISTRAL_API_KEY"] = "gTkvXwvzuMY7Rvi92LXGoqqnRK0WVj4u"
api_key = os.environ["MISTRAL_API_KEY"]

# Categories
phrases = ["Fitness", "Education", "Clothing"]

# Model
model = "mistral-embed"

# MistralClient instance with the API key
client = MistralClient(api_key=api_key)

# Embeddings for each phrase in the set
embeddings = []
for phrase in phrases:
    response = client.embeddings(model=model, input=[phrase])
    try:
        # Assuming `response` has a structure like `response.data[0].embedding`
        embedding_vector = response.data[0].embedding
        embeddings.append(embedding_vector)
    except Exception as e:
        print(f"Error retrieving embedding for '{phrase}': {e}")

def find_closest_match(input_text):
    # Compute embedding for input text
    input_embedding_response = client.embeddings(model=model, input=[input_text])
    try:
        input_embedding = input_embedding_response.data[0].embedding
    except Exception as e:
        print(f"Error retrieving embedding for input text '{input_text}': {e}")
        return None

    # Calculate cosine similarity between input embedding and each phrase's embedding
    similarities = []
    for phrase_embedding in embeddings:
        similarity = cosine_similarity([input_embedding], [phrase_embedding])[0][0]
        similarities.append(similarity)

    # Find the index of the closest match
    closest_index = np.argmax(similarities)
    closest_phrase = phrases[closest_index]

    return closest_phrase

"""# Usage
input_text = "weights"
closest_phrase = find_closest_match(input_text)

print(f"Input: {input_text}")
print(f"Closest Match: {closest_phrase}")"""