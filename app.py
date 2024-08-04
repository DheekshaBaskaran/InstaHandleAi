from flask import Flask, request, render_template_string
from postRetrieve import choose_category, determine_gender, determine_location, fetch_instagram_posts

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
            # Fetch Instagram posts for the influencer
            _, captions = fetch_instagram_posts(influencer_name)

            # Aggregate captions into one text
            aggregated_captions = " ".join(captions)

            # Choose a category based on the aggregated captions
            category = choose_category(aggregated_captions)

            # Determine gender based on the aggregated captions
            gender = determine_gender(aggregated_captions)

            # Determine location based on the aggregated captions
            location = determine_location(aggregated_captions)

        except Exception as e:
            # Print the error message if any exception occurs
            print(f"Error occurred: {e}")

    # Render the HTML template with the results
    return render_template_string(form_html, influencer_name=influencer_name, category=category, gender=gender, location=location)

if __name__ == '__main__':
    # Run the Flask application on localhost at port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
