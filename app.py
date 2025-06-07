from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/optimize", methods=["POST"])
def optimize():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    img = Image.open(file.stream).convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="WEBP", quality=80)
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/webp",
        as_attachment=True,
        download_name="optimized.webp"
    )

@app.route("/")
def home():
    return "✅ Flask Image Optimizer API is running"

@app.route("/upload")
def placeholder():
    return "Upload endpoint placeholder. Use /optimize for image optimization."
