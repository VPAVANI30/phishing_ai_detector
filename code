import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from flask import Flask, request, render_template_string
import requests

# Load dataset (optional if your app uses it)
df = pd.read_csv('dataset_full.csv')
label_col = df.columns[-1]
X = df.drop(columns=[label_col])
y = df[label_col]

# ✅ DOWNLOAD + LOAD MODEL
# Replace with your actual direct link to model.pkl
model_url = 'https://drive.google.com/file/d/1Pqje1SPmWHl2YAipDAuxBSzQLNHSTWzn/view?usp=sharing'  # Example: 'https://drive.google.com/uc?export=download&id=FILE_ID'

try:
    print("Downloading model...")
    r = requests.get(model_url)
    with open('model.pkl', 'wb') as f:
        f.write(r.content)
    print("Download complete. Loading model...")
    model = joblib.load('model.pkl')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# ✅ Set up Flask app
app = Flask(__name__)

# ✅ HTML for your form
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

# ✅ Flask route
@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        url = request.form['url']

        # 📝 Simulate extracting features from URL (replace with real feature extraction)
        features = [len(url), int('https' in url.lower()), int('.com' in url.lower()), len(url.split('/'))]

        # Make sure model is loaded
        if model:
            try:
                pred = model.predict([features])[0]
                if pred == 1:
                    result = "<span style='color: red;'>Phishing URL</span>"
                else:
                    result = "<span style='color: green;'>Legitimate URL</span>"
            except Exception as e:
                result = f"Error making prediction: {e}"
        else:
            result = "<span style='color: red;'>Model not loaded.</span>"

    return render_template_string(html, result=result)

# ✅ Run app
if __name__ == '__main__':
    app.run(debug=True)
