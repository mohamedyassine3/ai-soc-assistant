import os
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from preprocess import load_and_prepare


def main():
    X_train, X_test, y_train, y_test, enc = load_and_prepare(
        "data/UNSW_NB15_training-set.csv",
        "data/UNSW_NB15_testing-set.csv",
    )
    model = XGBClassifier(n_estimators=300, learning_rate=0.1, max_depth=6,
                          random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(classification_report(y_test, pred, target_names=["Normal", "Attaque"]))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/xgboost.joblib")
    joblib.dump(enc, "models/encoder.joblib")


if __name__ == "__main__":
    main()