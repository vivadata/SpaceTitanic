from sklearn.ensemble import RandomForestClassifier

from titanic.registry import upload_model


def _init_model():
    """Initialize the model"""
    return RandomForestClassifier(n_estimators=100, max_depth=10)


def train_model(X_train, y_train, model=None):
    """
    Train the model
    """
    if model is None:
        model = _init_model()
    model.fit(X_train, y_train)
    upload_model(model, "model")

    return model
