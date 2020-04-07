from flask import Flask, request
from google.cloud import kms_v1
import os
from google.api_core.exceptions import GoogleAPICallError
from base64 import b64encode, b64decode
from html import escape

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
kms = kms_v1.KeyManagementServiceClient()

# Adjust region based on your choice
# Create key ring and key in Cloud Console with these names
#  + Generated Key
#  + Protection Level: Software (or HSM, either will work)
#  + Purpose: Symmetric encrypt/decrypt
#  + Rotation period: Never (or leave at some period, will work fine, will just create new keys while otherwise idle)
# Give AppEngine Default Service Account access:
#  * Select key checkbox
#  * Open Info Panel (link at upper-right)
#  * Click "+ Add Member"
#  * add [PROJECT_NAME]@appspot.gserviceaccount.com (default app engine service account)
#  * with role "Cloud KMS CryptoKey Encrypter/Decrypter"
key_name = kms.crypto_key_path_path(os.environ['GOOGLE_CLOUD_PROJECT'], 'us-central1', 'example-key-ring', 'example-key')

@app.route('/')
def index():
    """Default page"""
    return """
    <html><head><title>KMS AppEngine Demo</title></head>
    <body>
        <form action="/encrypt" method="POST">
            <label for="message">Message:</label><input type="text" name="message" required>
            <input type="submit" value="Encrypt">
    </form>
    </body></html>
    """

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        response = kms.encrypt(key_name, request.form['message'].encode())
    except GoogleAPICallError as err:
        return "Something went wrong! " + err.message, 500
    return """
    <html><head><title>KMS AppEngine Demo</title></head>
    <body>
        <form action="/decrypt" method="POST">
            <label for="ciphertext">Ciphertext:</label>
            <textarea name="ciphertext" cols=40 rows=10>""" + \
            b64encode(response.ciphertext).decode("utf-8") + \
            """</textarea>
            <input type="submit" value="Decrypt">
        </form>
    </body></html>
    """

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        response = kms.decrypt(key_name, b64decode(request.form['ciphertext'].encode()))
    except GoogleAPICallError as err:
        return "Something went wrong! " + err.message, 500
    return """
    <html><head><title>KMS AppEngine Demo</title></head>
    <body>
        The message is: """ + \
        escape(response.plaintext.decode("utf-8")) + \
    """</body></html>"""




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)



