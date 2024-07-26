from flask import Flask, request, render_template_string
from postRetrieve import choose_category, determine_gender, fetch_instagram_posts, determine_location

app = Flask(__name__)

# HTML template for the form and displaying results
form_html = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Influencer Input</title>
  </head>
  <body>
    <h1>Enter the name of an influencer:</h1>
    <!-- Form to collect the influencer's name -->
    <form method="post">
      <input type="text" name="influencer_name" placeholder="Influencer Name" required>
      <input type="submit" value="Submit">
    </form>
    {% if influencer_name %}
    <!-- Display the entered influencer's name -->
    <p>You entered: {{ influencer_name }}</p>
    <!-- Display the results from processing -->
    <p>Category: {{ category }}</p>
    <p>Gender: {{ gender }}</p>
    <p>Location: {{ location }}</p>
    {% endif %}
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    influencer_name = None
    category = None
    gender = None
    location = None

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Retrieve the influencer's name from the form data
        influencer_name = request.form.get('influencer_name')

        # Try to fetch Instagram posts and categorize the content
        try:
            # Fetch Instagram posts and captions for the given influencer
            captions = fetch_instagram_posts(influencer_name)

            # Aggregate all captions into a single text string
            aggregated_captions = " ".join(captions)

            # Determine the category of the aggregated captions
            category = choose_category(aggregated_captions)

            # Determine the gender based on the aggregated captions
            gender = determine_gender(aggregated_captions)

            # Determine the location based on the aggregated captions
            location = determine_location(aggregated_captions)
        except Exception as e:
            # Handle any errors that occur during processing
            category = "Error processing request"
            gender = str(e)  # Display the error message for debugging
            location = "Unknown"

    # Render the HTML template with the provided results
    return render_template_string(form_html, influencer_name=influencer_name, category=category, gender=gender, location=location)

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
