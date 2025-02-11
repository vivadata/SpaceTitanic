from sklearn.ensemble import RandomForestClassifier

from titanic.registry import upload_model


def _init_model():
    """Initialize the model"""
    return RandomForestClassifier(n_estimators=100, random_state=42)


def train_model(X_train, y_train, model=None):
    """
    Train the model
    """
    if model is None:
        model = _init_model()
        upload_model(model, "model")
    model.fit(X_train, y_train)

    return model
