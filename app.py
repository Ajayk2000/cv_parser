from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import re
import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import your existing CV parsing functions
from cvparser import extract_text, extract_details, skills_list  # Adjust the import path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Parse the CV
            text = extract_text(file_path)
            details = extract_details(text, skills_list)
            os.remove(file_path)  # Clean up uploaded file
            return jsonify(details)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
