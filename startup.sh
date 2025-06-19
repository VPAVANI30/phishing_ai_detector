#!/bin/bash
echo "Downloading model..."
curl -L -o model.pkl "https://drive.google.com/uc?export=download&id=1Pqje1SPmWHl2YAipDAuxBSzQLNHSTWzn"
echo "Model downloaded. Starting web server..."
gunicorn app:app --bind 0.0.0.0:$PORT
