from flask import Flask, request, render_template_string, send_from_directory
import os
import subprocess
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
CERTIF_UPLOAD_FOLDER = './certificates'
os.makedirs(CERTIF_UPLOAD_FOLDER, exist_ok=True)

# Enable CORS
CORS(app)

# HTML template for user input
HTML_CERTIF = """
<!doctype html>
<html lang="en">
<head>
    <title>Certificate Generator</title>
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
    </style>
</head>
<body>
    <h1>Generate Your Certificate</h1>
    <form action="/certificate" method="post">
        <label for="common_name">Common Name (e.g., domain.com):</label>
        <input type="text" id="common_name" name="common_name" required>

        <label for="country">Country (2-letter code):</label>
        <input type="text" id="country" name="country" required>

        <label for="state">State or Province:</label>
        <input type="text" id="state" name="state" required>

        <label for="locality">Locality (e.g., city):</label>
        <input type="text" id="locality" name="locality" required>

        <label for="organization">Organization Name:</label>
        <input type="text" id="organization" name="organization" required>

        <label for="organizational_unit">Organizational Unit:</label>
        <input type="text" id="organizational_unit" name="organizational_unit" required>

        <button type="submit">Generate Certificate</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CERTIF)

@app.route('/certificate', methods=['POST'])
def generate():
    # Collect form data
    common_name = request.form['common_name']
    country = request.form['country']
    state = request.form['state']
    locality = request.form['locality']
    organization = request.form['organization']
    organizational_unit = request.form['organizational_unit']

    # File paths
    key_path = os.path.join(CERTIF_UPLOAD_FOLDER, f"{common_name}_key.pem")
    csr_path = os.path.join(CERTIF_UPLOAD_FOLDER, f"{common_name}.csr")
    cert_path = os.path.join(CERTIF_UPLOAD_FOLDER, f"{common_name}.crt")

    # OpenSSL commands
    try:
        # Generate a private key
        subprocess.run(
            [r'C:\Program Files\OpenSSL-Win64\bin\openssl.exe', 'genrsa', '-out', key_path, '2048'], check=True
        )

        # Create a CSR
        subprocess.run([
            r'C:\Program Files\OpenSSL-Win64\bin\openssl.exe', 'req', '-new', '-key', key_path, '-out', csr_path,
            '-subj', f"/C={country}/ST={state}/L={locality}/O={organization}/OU={organizational_unit}/CN={common_name}"
        ], check=True)

        # Generate a self-signed certificate
        subprocess.run([
            r'C:\Program Files\OpenSSL-Win64\bin\openssl.exe', 'x509', '-req', '-in', csr_path, '-signkey', key_path,
            '-out', cert_path, '-days', '365'
        ], check=True)
    except subprocess.CalledProcessError as e:
        return f"<h1>Error</h1><p>An error occurred while generating the certificate: {str(e)}</p>"

    # Success page
    SUCCESS_HTML = f"""
    <!doctype html>
    <html lang="en">
    <head>
        <title>Certificate Generated</title>
        <style>
            body {{
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
            }}
            h1 {{
                color: #66bb6a;
            }}
            .container {{
                background-color: #29293d;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                width: 400px;
                text-align: center;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
            }}
            a {{
                color: #ffa726;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            button {{
                background-color: #ffa726;
                color: #1e1e2f;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                margin-top: 15px;
            }}
            button:hover {{
                background-color: #ff9800;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Certificate Generated!</h1>
            <p>Your certificate and related files are ready for download:</p>
            <ul>
                <li><a href="/download/{common_name}_key.pem">Download Private Key</a></li>
                <li><a href="/download/{common_name}.csr">Download CSR</a></li>
                <li><a href="/download/{common_name}.crt">Download Self-Signed Certificate</a></li>
            </ul>
            <button onclick="window.location.href='/'">Generate Another Certificate</button>
        </div>
    </body>
    </html>
    """
    return SUCCESS_HTML

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(CERTIF_UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
