from flask import Flask, request, render_template_string, send_file
import pandas as pd
import os
import re
from io import BytesIO
import random
import openpyxl

# HTML Form with design
HTML_ANONYM = """
<!doctype html>
<html lang="en">
<head>
    <title>Document Anonymizer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1e1e2f;
            color: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        h1 {
            color: #ffa726;
        }
        form {
            background-color: #29293d;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            width: 300px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #444;
            border-radius: 5px;
            background-color: #1e1e2f;
            color: #f5f5f5;
        }
        button {
            background-color: #ffa726;
            color: #1e1e2f;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background-color: #ff9800;
        }
        .download-link {
            margin-top: 15px;
            text-align: center;
        }
        .download-link a {
            color: #ffa726;
            text-decoration: none;
        }
        .download-link a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Document Anonymizer</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <label for="file">Upload CSV or Excel File:</label>
        <input type="file" id="file" name="file" required>

        <button type="submit">Anonymize & Download</button>
    </form>
    
    {% if download_link %}
        <div class="download-link">
            <p>Your file is ready! <a href="{{ download_link }}" download>Download it here</a></p>
        </div>
    {% endif %}
</body>
</html>
"""

app = Flask(__name__)

# Directory to save uploaded and anonymized files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define regex patterns for common types of data
patterns = {
    'name': r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$',  # Simple name pattern
    'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',  # Email pattern
    'phone': r'^\d{10}$',  # 10-digit phone number
    'address': r'\d{1,5}\s[A-Za-z]+\s[A-Za-z]+',  # Simple street address
}

def identify_column_type(df):
    column_types = {}
    for column in df.columns:
        # Determine the number of rows to sample (up to 5, or less if fewer rows exist)
        sample_size = min(5, len(df))
        sample_data = df[column].astype(str).sample(sample_size, random_state=1).tolist()
        for label, pattern in patterns.items():
            if any(re.match(pattern, item) for item in sample_data):
                column_types[column] = label
                break
        else:
            column_types[column] = 'unknown'
    return column_types


@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            # Determine the file extension and process accordingly
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
                output_format = 'csv'
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file, skiprows=0, dtype=str)  # Do not skip the first row
                output_format = 'excel'
            else:
                return "Unsupported file format. Please upload a CSV or Excel file."

            # Identify column types
            column_types = identify_column_type(df)
            print("\nIdentified column types:")
            for col, col_type in column_types.items():
                print(f"{col}: {col_type}")

            # Anonymize the data (simple masking of text columns)
            for column in df.columns:
                if column_types.get(column) in ['name', 'email', 'address', 'phone']:
                    df[column] = df[column].apply(lambda x: '****' if pd.notnull(x) else x)

            # Save the anonymized data to the appropriate format
            output = BytesIO()
            if output_format == 'csv':
                df.to_csv(output, index=False)
                output.seek(0)  # Reset buffer position
                file_extension = 'csv'
                mimetype = 'text/csv'
            elif output_format == 'excel':
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)  # Reset buffer position
                file_extension = 'xlsx'
                mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            else:
                raise ValueError("Unsupported file format")  # Safety check for unexpected formats

            # Ensure file_extension is properly assigned
            assert file_extension in ['csv', 'xlsx'], "File extension is not properly set!"

            # Create a filename for download
            download_filename = f"anonymized_file.{file_extension}"

            # Serve the file to the client
            return send_file(
                output,
                as_attachment=True,
                download_name=download_filename,
                mimetype=mimetype
            )
 
    return render_template_string(HTML_ANONYM, download_link=download_link)


if __name__ == "__main__":
    app.run(debug=True)
