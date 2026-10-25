import os
import base64
import traceback
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

UPLOAD_FOLDER = 'img_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        if not GEMINI_API_KEY:
            return jsonify({'error': 'GEMINI_API_KEY set nahi hai'}), 500

        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        lat = request.form.get('latitude', 'N/A')
        lon = request.form.get('longitude', 'N/A')

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"

        current_time = datetime.now().strftime("%d %B %Y, %I:%M %p")

        prompt_text = f"""
        You are an expert civic infrastructure analyst. Inspect this image of a civic hazard (pothole, garbage dump, broken street light, etc.).
        Location Coordinates: Latitude {lat}, Longitude {lon}.
        Current Date and Time: {current_time}. Use exactly this date and time in the complaint letter. Do not invent any other date.

        Do not use markdown symbols like ** or #. Use plain text only.

        Provide your response strictly in the following format:
        1. Issue Type: (e.g., Severe Pothole / Open Garbage Dump)
        2. Severity Score: (Integer from 1 to 10)
        3. Formal Complaint Letter: (A ready-to-dispatch formal complaint letter addressed to the Municipal Commissioner, including the date and time given above, GPS coordinates, hazard description, and a request for urgent repair).
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": file.mimetype or "image/jpeg",
                            "data": image_data
                        }
                    }
                ]
            }]
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        if os.path.exists(filepath):
            os.remove(filepath)

        if 'candidates' in result:
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({
                'success': True,
                'analysis': ai_response,
                'location': {'lat': lat, 'lon': lon}
            })
        else:
            print("Gemini API Error Response:", result)
            return jsonify({'error': str(result)}), 500

    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)