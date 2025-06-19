import os
import pandas as pd
import joblib
import requests
from flask import Flask, request, render_template_string

# ✅ Load dataset if needed
df = pd.read_csv('dataset_full.csv')  # Or remove if not required

# ✅ Download + cache model
model_url = 'https://drive.google.com/uc?export=download&id=1Pqje1SPmWHl2YAipDAuxBSzQLNHSTWzn'
model_path = 'model.pkl'

if not os.path.exists(model_path):
    print("Downloading model...")
    response = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(response.content)
    print("Model downloaded.")

# ✅ Load model
model = joblib.load(model_path)

# ✅ Set up Flask app
app = Flask(__name__)

# ✅ HTML form
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WEB PHISH GUARD</title>
    <style>
        body {
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 90%;
        }
        h1 {
            color: #1f4037;
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            margin-top: 20px;
            padding: 12px 20px;
            font-size: 16px;
            background: #1f4037;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background: #163529;
        }
        .result {
            margin-top: 20px;
            font-size: 1.2em;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phishing URL Detector</h1>
        <form method="post">
            <input type="text" name="url" placeholder="Enter a URL (simulated check)" required>
            <button type="submit">Check URL</button>
        </form>
        <div class="result">
            {{ result|safe }}
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        url = request.form['url']
        features = [len(url), int('https' in url.lower()), int('.com' in url.lower()), len(url.split('/'))]

        try:
            pred = model.predict([features])[0]
            if pred == 1:
                result = "<span style='color: red;'>Phishing URL</span>"
            else:
                result = "<span style='color: green;'>Legitimate URL</span>"
        except Exception as e:
            result = f"Error: {e}"

    return render_template_string(html, result=result)

# No need for app.run() — Gunicorn handles it

