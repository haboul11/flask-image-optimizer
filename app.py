from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Flask Image Optimizer API is running on Render!'

@app.route('/optimize', methods=['POST'])
def optimize_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        img = Image.open(image_file)
        buffer = io.BytesIO()
        img.save(buffer, format='WEBP', quality=70)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return jsonify({'optimized_image': img_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
