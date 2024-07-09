from textCategortization import find_closest_match
from imgDesc import query



json_caption = query("test.png")
closest_phrase = find_closest_match(json_caption[0]['generated_text'])

print(f" {json_caption}")
print(f"Closest Match: {closest_phrase}")

