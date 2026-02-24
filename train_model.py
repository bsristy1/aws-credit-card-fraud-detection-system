import tarfile
import joblib
import boto3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score





def get_data(bucket_name, file_key):
    path = f"s3://{bucket_name}/{file_key}"
    print(f"Retrieving dataset from {path}...")
    return pd.read_csv(path)

def balance_classes(data):


    fraud_txns = data[data.Class == 1]
    clean_txns = data[data.Class == 0]



    clean_downsampled = resample(
        clean_txns,
        replace=False,
        n_samples=len(fraud_txns),
        random_state=42
    )
    
    return pd.concat([fraud_txns, clean_downsampled])

def train_and_evaluate(processed_data):
    X_features = processed_data.drop("Class", axis=1)
    y_target = processed_data["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_features, y_target, test_size=0.2, random_state=42
    )



    classifier = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    classifier.fit(X_train, y_train)
    preds = classifier.predict_proba(X_test)[:, 1]
    score = roc_auc_score(y_test, preds)
    print(f"Validation ROC-AUC: {score:.4f}")

    
    
    return classifier

def package_model(trained_model):
    joblib.dump(trained_model, "model.joblib")
    
    with open("requirements.txt", "w") as req_file:
        req_file.write("xgboost\n")
    
    with tarfile.open("model.tar.gz", "w:gz") as tar:

        tar.add("model.joblib")
        tar.add("requirements.txt")
    
    print("Model artifacts compressed and ready for S3 upload.")





if __name__ == "__main__":
    BUCKET_NAME = "bhargav-fraud-detection-2026"
    FILE_PATH = "raw/creditcard.csv"

    raw_df = get_data(BUCKET_NAME, FILE_PATH)
    balanced_df = balance_classes(raw_df)
    xgb_model = train_and_evaluate(balanced_df)
    package_model(xgb_model)