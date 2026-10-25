# CivicAlert AI

Upload a photo of a civic hazard (pothole, garbage dump, broken street light) and get:
- Issue type
- Severity score (1-10)
- A ready-to-send formal complaint letter with date, time and GPS location

Built with Python, Flask and the Google Gemini API.

## Features
- Image upload with GPS location capture
- AI-based hazard analysis
- Auto-generated formal complaint letter
- One-click email draft to the municipal authority

## How to run

1. Clone the repo
   ```
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Get a free API key from Google AI Studio (https://aistudio.google.com) and set it

   Windows PowerShell:
   ```
   $env:GEMINI_API_KEY="your_key_here"
   ```
   Mac/Linux:
   ```
   export GEMINI_API_KEY="your_key_here"
   ```
4. Run the app
   ```
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser

## Note
The free Gemini API tier has a daily request limit, so each user should use their own API key.
The municipal email address in the app is a placeholder. Replace it with your city's official grievance email.