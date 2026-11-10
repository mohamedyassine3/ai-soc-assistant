import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

CAT_COLS = ["proto", "service", "state"]


def load_and_prepare(train_path, test_path):
    train = (pd.read_csv(train_path).drop(columns=["id"], errors="ignore")
             .drop_duplicates().reset_index(drop=True))
    test = (pd.read_csv(test_path).drop(columns=["id"], errors="ignore")
            .drop_duplicates().reset_index(drop=True))

    y_train, y_test = train["label"], test["label"]
    X_train = train.drop(columns=["label", "attack_cat"])
    X_test = test.drop(columns=["label", "attack_cat"])

    enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X_train[CAT_COLS] = enc.fit_transform(X_train[CAT_COLS])
    X_test[CAT_COLS] = enc.transform(X_test[CAT_COLS])
    return X_train, X_test, y_train, y_test, enc