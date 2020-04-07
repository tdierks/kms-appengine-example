A sample app which demonstrates use of Google Cloud Key Management System from a Python AppEngine app.

See instructions in main.py on creating a suitable KMS key with the console or you can create from the command line with:
```
gcloud kms keyrings create example-key-ring --location=global
gcloud kms keys create example-key --purpose=encryption --keyring=example-key-ring --location=global
```

To run from Cloud Shell:
```
python3 -m venv env
source env/bin/activate
pip install  -r requirements.txt
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) python3 main.py
```
When running locally from Cloud Shell, the app will use your personal identity for accessing KMS;
when running on App Engine it will use the App Engine default service account
([PROJECT_NAME]@appspot.gserviceaccount.com). By default these are both authorized to use KMS keys
in a project you've created (you because you're the project owner and the App Engine service account
because it defaults to being a project editor).

You can deploy to App Engine with `gcloud app deploy`
