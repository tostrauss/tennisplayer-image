# TennisPlayer Image App

The **TennisPlayer Image App** is a web application built using Flask that interacts with OpenAI's image generation API to create customized images of tennis players. The app stores generated images locally and maintains a record of them in a pickled format for later retrieval. This project showcases the integration of Flask, OpenAI's API, and Python libraries for building a full-featured image generation service.

## Features

- **Generate Images**: Create tennis player images based on customizable prompts using OpenAI's DALL-E model.
- **Save Locally**: Store generated images locally with dynamic filenames.
- **Pickle Storage**: Save the generated images and configuration data as a serialized pickle file.
- **REST API**: Exposes a `/generate-image` endpoint for creating images via HTTP POST requests.
- **Configuration Management**: Uses `config.json` and `.env` for customizable application settings.

## Technologies Used

- **Python**: Core programming language used for backend logic.
- **Flask**: Lightweight web framework for creating RESTful APIs.
- **OpenAI API**: Integrates with OpenAI's DALL-E model to generate images.
- **Pillow**: For image manipulation and processing.
- **Requests**: For handling HTTP requests to download images.
- **Pickle**: For serializing and deserializing image data.
- **dotenv**: For securely loading environment variables.

## Prerequisites

- Python 3.7 or higher
- An OpenAI API key with the necessary image generation permissions
- Git (for version control)

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/tennisplayer-image-app.git
   cd tennisplayer-image-app

