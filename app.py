from flask import Flask, request, jsonify
from transformers import pipeline
import requests
import json
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the API endpoint to handle POST requests
@app.route('/', methods=['POST'])
def scrape_cooked_text_api():
    return "Hello"

# Define the API endpoint to handle POST requests
@app.route('/get_tendancy', methods=['POST'])
def scrape_cooked_text_api():
    data = request.json  # Assuming JSON data with a "url" field containing the target URL
    url = data.get('url', None)

    content = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}

    # Send a GET request to the URL and fetch the HTML content
    response = requests.get(url, headers=headers)
     # Raise an exception for any HTTP errors
    print(response.raise_for_status())

    json_content = json.loads(response.content)

    for item in json_content["post_stream"]["posts"]:
        soup = BeautifulSoup(item["cooked"], "html.parser")
        content.append(soup.find("p").text)

    classifier = pipeline(task="sentiment-analysis")
    preds = classifier(content)
    preds = [{"score": round(pred["score"], 4), "label": pred["label"]}
            for pred in preds]
    print(preds)

    positive = 0
    negative = 0
    counter = 0
    for pred in preds:
        if pred["label"] == "POSITIVE":
            positive += 1
        if pred["label"] == "NEGATIVE":
            negative += 1
        counter += 1

   
    if url is None:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        return jsonify({'success': True, 'tendancy': positive / counter * 100})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, ,host='0.0.0.0')
