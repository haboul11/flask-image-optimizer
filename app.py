from flask import Flask, request, jsonify
from PIL import Image
import requests
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "🧠 MidJourney Image Optimizer API is running!"

@app.route('/optimize-upload', methods=['POST'])
def optimize_and_upload():
    data = request.json
    image_url = data.get('image_url')
    keyword = data.get('keyword', 'image')

    if not image_url:
        return jsonify({"error": "Missing image_url"}), 400

    # Download image
    response = requests.get(image_url)
    image = Image.open(io.BytesIO(response.content))

    # Convert to WebP
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="WEBP", quality=80)
    buffer.seek(0)

    # Upload to WordPress
    wp_url = "https://recipescookery.com/wp-json/wp/v2/media"
    username = "h.aboulfadam"
    password = "mMSV Jpi7 mu2o Lxxp IIMl WFZu"
    auth = base64.b64encode(f"{username}:{password}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Disposition": f'attachment; filename="{keyword}-webp.webp"',
        "Content-Type": "image/webp"
    }

    upload_response = requests.post(wp_url, headers=headers, data=buffer.getvalue())
    result = upload_response.json()
    return jsonify(result)
