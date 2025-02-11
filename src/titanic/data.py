import os

import pandas as pd
from google.cloud import bigquery
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from titanic.params import BQ_DATASET, BQ_TABLE, GCP_PROJECT_ID
from titanic.registry import upload_model

if not os.path.exists("credentials/service-account.json"):

    raise ImportError(
        """Service account credentials not found,\
        \nplease make sure the credentials are available in the credentials folder\
        \nand named as service-account.json"""
    )
bq_client = bigquery.Client.from_service_account_json(
    "credentials/service-account.json"
)


def load_data(cache: bool = True) -> pd.DataFrame:
    """
    Load Raw data from BigQuery
    """
    dataset_ref = bigquery.DatasetReference(GCP_PROJECT_ID, BQ_DATASET)
    table_ref = dataset_ref.table(BQ_TABLE)
    table = bq_client.get_table(table_ref)
    df = bq_client.list_rows(table).to_dataframe()
    if cache:
        df.to_csv("data/raw_data.csv", index=False)
    return df


def create_X_y(df: pd.DataFrame, y: bool = False) -> tuple[pd.DataFrame, pd.Series]:
    """
    Create X and y from the dataframe
    """
    if y:
        y = df.pop("Transported").astype(int)
    # (a) Extract Deck, Cabin_num, Side from the 'Cabin' column
    df[["Deck", "CabinNum", "Side"]] = df["Cabin"].str.split("/", expand=True)
    df.drop(columns=["Cabin"], inplace=True)  # We won't use the original Cabin anymore
    df["CabinNum"] = pd.to_numeric(df["CabinNum"], errors="coerce")

    # (b) Drop columns that may not be useful (like PassengerId, Name)
    df.drop(columns=["PassengerId", "Name", "CabinNum"], inplace=True, errors="ignore")

    X = df.copy()
    return X, y


def _create_preproc_pip(X: pd.DataFrame) -> Pipeline:
    """
    Instantiate a preprocessor pipeline
    """
    num_cols = X.select_dtypes(include="number").columns.tolist()
    numeric_transformer = Pipeline(
        steps=[
            ("num_imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    cat_cols = X.select_dtypes(include="object").columns.tolist()
    categorical_transformer = Pipeline(
        steps=[
            ("cat_imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    ).set_output(transform="pandas")
    return preprocessor


def preprocess_data(
    X_train, X_test=None, preprocessor: Pipeline = None
) -> pd.DataFrame:
    """
    Preprocess data
    """
    if preprocessor is None:
        preprocessor = _create_preproc_pip(X_train)
        X_prep = preprocessor.fit(X_train)
        upload_model(preprocessor, "preprocessor")
    X_prep = preprocessor.transform(X_train)
    if X_test is not None:
        X_test_prep = preprocessor.transform(X_test)
        return X_prep, X_test_prep
    return X_prep
