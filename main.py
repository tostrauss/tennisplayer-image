from flask import Flask, request, jsonify, render_template
import os
import requests
import pickle
from dotenv import load_dotenv
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai
from flask_wtf.csrf import CSRFProtect

# Load environment variables securely
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app and configure rate limiting
app = Flask(__name__)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to store pickle data
PICKLE_PATH = 'static/generated_images/records.pkl'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
@csrf.exempt  # If CSRF protection is needed for specific routes, handle with care.
@limiter.limit("5 per minute")
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        logging.warning("No prompt provided by user.")
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        # Use OpenAI API to generate an image based on the prompt
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        image_url = response['data'][0]['url']
        filename = f"static/generated_images/tennisplayer_image.png"

        # Download and save the image locally
        image_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)

        # Log successful generation
        logging.info(f"Image generated and saved: {filename}")

        # Save the record using pickle
        record = {'prompt': prompt, 'filename': filename, 'url': image_url}
        existing_records = []
        if os.path.exists(PICKLE_PATH):
            with open(PICKLE_PATH, 'rb') as f:
                existing_records = pickle.load(f)

        existing_records.append(record)
        with open(PICKLE_PATH, 'wb') as f:
            pickle.dump(existing_records, f)

        return jsonify({'files': [filename]})

    except openai.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 400
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image: {e}")
        return jsonify({'error': 'Failed to download the generated image. Please try again later.'}), 400
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({'error': 'An unexpected error occurred. Please contact support.'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)  # Production configuration
