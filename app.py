import os
os.makedirs("saved_images", exist_ok=True)

from flask import Flask, render_template, request, send_from_directory
import cv2
import base64
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Smile Detection Function (NO drawing, just math)
def detect_smile(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    
    smiles = smile_cascade.detectMultiScale(
        gray,
        scaleFactor=1.8,
        minNeighbors=20
    )

    if len(smiles) > 0:
        largest_smile = max(smiles, key=lambda s: s[2] * s[3])
        x, y, w, h = largest_smile
        smile_area = w * h
        total_area = img.shape[0] * img.shape[1]
        smile_percent = (smile_area / total_area) * 100
        return True, round(smile_percent, 2)
    
    return False, 0.0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture", methods=["POST"])
def capture():
    data = request.get_json()
    img_data = data["image"].split(",")[1]
    nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    is_smile, smile_score = detect_smile(img)

    if is_smile:
        filename = datetime.now().strftime("smile_%Y%m%d_%H%M%S.png")
        filepath = os.path.join("saved_images", filename)
        cv2.imwrite(filepath, img)

        return {
            "status": "success",
            "message": f"Smile detected! Intensity: {smile_score:.2f}%",
            "smile_score": smile_score,
            "image_url": f"/images/{filename}"
        }
    else:
        return {
            "status": "error",
            "message": "No smile detected. Try again!",
            "smile_score": 0.0
        }

@app.route("/images/<filename>")
def send_image(filename):
    return send_from_directory("saved_images", filename)

if __name__ == "__main__":
    os.makedirs("saved_images", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)