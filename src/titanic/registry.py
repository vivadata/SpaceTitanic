import os

import joblib
from google.cloud import storage

from titanic.params import GCP_BUCKET, GCP_PROJECT_ID


def upload_model(model, model_name: str):
    """
    Upload the model to GCS
    """
    client = storage.Client.from_service_account_json(
        "credentials/service-account.json"
    )
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


def load_model(model_name: str, use_cache: bool = True):
    """
    Load the model from GCS
    """

    if not os.path.exists("models"):
        os.makedirs("models")
    model_path = os.path.join("models", model_name + ".joblib")
    if os.path.exists(model_path) and use_cache:
        model = joblib.load(model_path)
        print(f" 📡 {model_name} loaded from cache")
        return model
    client = storage.Client.from_service_account_json(
        "credentials/service-account.json"
    )
    bucket = client.bucket(GCP_BUCKET)
    blob = bucket.blob(model_name + ".joblib")
    model_path = os.path.join("models", model_name + ".joblib")
    blob.download_to_filename(model_path)
    model = joblib.load(model_path)
    print(f" 📡 {model_name} loaded from GCS")
    with open(model_path, "wb") as model_file:
        joblib.dump(model, model_file)
    return model
