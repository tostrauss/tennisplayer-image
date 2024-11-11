from flask import Flask, request, jsonify, render_template
import openai
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        # Use OpenAI API to generate an image based on the prompt
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size='1024x1024'
        )

        image_url = response['data'][0]['url']
        filename = f"static/generated_images/tennisplayer_image.png"

        # Download and save the image locally
        image_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)

        return jsonify({'files': [filename]})

    except openai.OpenAIError as e:
        return jsonify({'error': str(e)}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

