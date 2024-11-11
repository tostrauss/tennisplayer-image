from flask import Flask, request, jsonify
import openai
import json
from io import BytesIO
from PIL import Image
import requests
import pickle
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

def pickle_data(saved_files, config_data):
    """
    Pickles the downloaded image files and the configuration file data.
    """
    data_to_pickle = {
        'config': config_data,
        'images': []
    }

    for filename in saved_files:
        with open(filename, 'rb') as image_file:
            image_data = image_file.read()
            data_to_pickle['images'].append({
                'filename': filename,
                'data': image_data
            })

    pickle_filename = 'image_data.pkl'
    with open(pickle_filename, 'wb') as pickle_file:
        pickle.dump(data_to_pickle, pickle_file)

    print(f'Data pickled and saved as {pickle_filename}')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt', 'A tennis player image')
    model = data.get('model', config['default_model'])
    size = data.get('size', config['image_size'])
    n = data.get('n', 1)
    quality = data.get('quality', config.get('quality', 'standard'))
    style = data.get('style', config.get('style', None))
    filename_base = config.get('filename_base', 'tennisplayer_image')
    timeout = config.get('timeout', 30)
    if not data:
        return jsonify({"error": 'A tennis player image'}), 400

    prompt = data.get('prompt', 'A tennis player image')

    # Append style to the prompt if provided
    if style:
        prompt += f", in {style} style"

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=n,
            size=size
        )
        
        image_urls = [item['url'] for item in response['data']]
        saved_files = []

        for idx, image_url in enumerate(image_urls):
            image_data = requests.get(image_url, timeout=timeout).content
            filename = f"{filename_base}{idx + 1}.png"
            with open(filename, 'wb') as image_file:
                image_file.write(image_data)
            saved_files.append(filename)
            print(f'Image saved as {filename}')
        
        # Pickle the images and config data
        pickle_data(saved_files, config)

        return jsonify({'message': 'Images generated and saved successfully', 'files': saved_files})

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
