from boltiotai import openai
import os
from flask import Flask, render_template_string, request

# Set OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']


def generate_tutorial(components):
    response = openai.Images.create(
        prompt=components,
        model="dall-e-3",
        size="1024x1024",
        response_format="url"
    )
    image_url = response['data'][0]['url']
    return image_url


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    output = ""

    if request.method == 'POST':
        components = request.form['components']
        output = generate_tutorial(components)

    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Infinite Image Generator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
<div class="container">
    <h1 class="my-4">Custom Image Generator</h1>

    <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
        <div class="mb-3">
            <label for="components" class="form-label">Textual Description of the Image:</label>
            <input type="text"
                   class="form-control"
                   id="components"
                   name="components"
                   placeholder="Enter the Description (Ex: A Lion in a Cage)"
                   required>
        </div>
        <button type="submit" class="btn btn-primary">Share with the Image</button>
    </form>

    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            Output:
            <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
        </div>
        <div class="card-body">
            <p id="output" style="white-space: pre-wrap;"></p>
            <img id="myImage" src="" style="width: auto; height: 300px;">
        </div>
    </div>
</div>

<script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
        ''',
        output=output
    )


@app.route('/generate', methods=['POST'])
def generate():
    components = request.form['components']
    return generate_tutorial(components)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)