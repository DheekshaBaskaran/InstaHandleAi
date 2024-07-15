from textCategortization import chooseCategory
from imgDesc import query
import os



def categorize(saved_images):
    # Step 1: Generate descriptions for each image
    descriptions = []
    for image_file in saved_images:
        image_path = os.path.join("temp/images", image_file)  # Ensure the path includes the directory
        json_caption = query(image_path)
        descriptions.append(json_caption[0]['generated_text'])

    # Step 2: Combine all descriptions
    combined_descriptions = " ".join(descriptions)

    # Step 3: Categorize the combined descriptions
    closest_phrase = chooseCategory(combined_descriptions)

    print(f"Combined Descriptions: {combined_descriptions}")
    print(f"Closest Match: {closest_phrase}")

