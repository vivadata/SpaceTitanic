import os

import joblib
from google.cloud import storage

from titanic.params import GCP_BUCKET, GCP_PROJECT_ID


def upload_model(model, model_name: str):
    """
    Upload the model to GCS
    """
    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.bucket(GCP_BUCKET)
    blob = bucket.blob(model_name + ".joblib")
    model_path = os.path.join("models", model_name + ".joblib")
    with open(model_path, "wb") as model_file:
        joblib.dump(model, model_file)
    blob.upload_from_filename(model_path)

    # Optional: Remove the local model file after uploading
    os.remove(model_path)
    print(f" 🚀 {model_name} uploaded to GCS")
    return f" {model_name} uploaded to GCS"
