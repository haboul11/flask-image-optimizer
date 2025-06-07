from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask Image Optimizer API is running"

@app.route("/upload")
def upload_placeholder():
    return "Upload endpoint placeholder. Use /optimize for image optimization."

@app.route("/optimize", methods=["POST"])
def optimize():
    if "image" not in request.files:
        return "❌ No image file found in request", 400

    file = request.files["image"]
    if file.filename == "":
        return "❌ Empty filename", 400

    try:
        # 🖼️ Load the uploaded image
        img = Image.open(file.stream).convert("RGB")

        # 💾 Save it as WebP to a memory buffer
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=80)
        buffer.seek(0)

        # 🔁 Return it as a downloadable WebP file
        filename_base = file.filename.rsplit('.', 1)[0]
        return send_file(
            buffer,
            mimetype="image/webp",
            as_attachment=True,
            download_name=filename_base + ".webp"
        )

    except Exception as e:
        return f"❌ Failed to convert image to WebP: {str(e)}", 500
