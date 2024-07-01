from flask import Flask, request, send_from_directory, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def find_long_cells(file_path, char_limit):
    xls = pd.ExcelFile(file_path)
    long_cells = []
    
    for sheet_name in xls.sheet_names:
        sheet = pd.read_excel(xls, sheet_name=sheet_name)
        for row_idx, row in sheet.iterrows():
            for cell in row:
                if isinstance(cell, str) and len(cell) > char_limit:
                    long_cells.append({"row": row_idx + 1, "cell": cell})  # Store row number and cell content
    
    return long_cells

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'char_limit' not in request.form:
        return jsonify({'error': 'No file part or character limit provided'}), 400
    file = request.files['file']
    char_limit = int(request.form['char_limit'])
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        results = find_long_cells(file_path, char_limit)
        return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
