from flask import Flask, request, jsonify
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask Image Optimizer API is running on Render!"

@app.route("/optimize", methods=["GET", "POST"])
def optimize_image():
    if request.method == "GET":
        return "📨 Send a POST request with an image to /optimize to get an optimized version."

    if 'image' not in request.files:
        return jsonify({"error": "No image file found in request."}), 400

    file = request.files['image']

    try:
        img = Image.open(file.stream)
        img_format = img.format or 'JPEG'

        # Optimize image
        optimized_io = io.BytesIO()
        img.save(optimized_io, format=img_format, optimize=True, quality=70)
        optimized_io.seek(0)

        # Send back the optimized image
        return (
            optimized_io.read(),
            200,
            {
                "Content-Type": f"image/{img_format.lower()}",
                "Content-Disposition": f"inline; filename=optimized.{img_format.lower()}"
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional route for /upload to avoid 404
@app.route("/upload", methods=["GET", "POST"])
def upload():
    return "🔁 Upload endpoint placeholder. Use /optimize for image optimization."

# Required for gunicorn to find the app
if __name__ == "__main__":
    app.run(debug=True)
