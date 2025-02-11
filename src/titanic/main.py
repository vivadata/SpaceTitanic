import logging

from sklearn.model_selection import train_test_split

from titanic.data import create_X_y, load_data, preprocess_data
from titanic.model import train_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()


def main():
    logger.info("🚀 Titanic ML Pipeline 🚀")
    logger.info("Loading data...")
    df = load_data()
    X, y = create_X_y(df, y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    logger.info("Preprocessing data...")
    X_train_prep, X_test = preprocess_data(X_train, X_test)
    logger.info("✅ Data loaded and preprocessed successfully")
    logger.info("Training model...")
    model = train_model(X_train_prep, y_train)
    logger.info("✅ Model trained successfully")
    logger.info(f"Score on Train: {round(model.score(X_train_prep, y_train),4)}")
    logger.info(f"Score on Test: {round(model.score(X_test, y_test),4)}")


if __name__ == "__main__":
    main()
