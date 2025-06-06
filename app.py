from flask import Flask, request, send_file
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return '<h3>✅ Flask Image Optimizer API is running on Render!</h3>'

@app.route("/optimize", methods=["POST"])
def optimize_image():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    if file.filename == "":
        return "No selected file", 400

    try:
        # Open image
        img = Image.open(file.stream).convert("RGB")

        # Compress and convert to WebP
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=80)  # you can try 70-80 for better compression
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/webp",
            as_attachment=True,
            download_name=os.path.splitext(file.filename)[0] + ".webp"
        )

    except Exception as e:
        return f"Error processing image: {str(e)}", 500
