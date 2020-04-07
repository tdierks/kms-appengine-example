A sample app which demonstrates use of Google Cloud Key Management System from a Python AppEngine app.

See instructions in main.py on creating a suitable KMS key

To run from Cloud Shell:
```
python3 -m venv env
source env/bin/activate
pip install  -r requirements.txt
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) python3 main.py
```

You can deploy to App Engine with `gcloud app deploy`
