import os
import sys

import joblib
import numpy as np
from sklearn.metrics import precision_score, recall_score

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from preprocess import load_and_prepare, CAT_COLS

TRAIN = "data/UNSW_NB15_training-set.csv"
TEST = "data/UNSW_NB15_testing-set.csv"


def test_pas_de_fuite_de_donnees():
    X_train, X_test, *_ = load_and_prepare(TRAIN, TEST)
    for col in ("label", "attack_cat"):
        assert col not in X_train.columns
        assert col not in X_test.columns


def test_donnees_propres():
    X_train, X_test, *_ = load_and_prepare(TRAIN, TEST)
    for X in (X_train, X_test):
        assert not X.isnull().any().any()
        assert np.isfinite(X.to_numpy(dtype=float)).all()


def test_memes_colonnes_train_test():
    X_train, X_test, *_ = load_and_prepare(TRAIN, TEST)
    assert list(X_train.columns) == list(X_test.columns)


def test_qualite_minimale_du_modele():
    model = joblib.load("models/xgboost.joblib")
    _, X_test, _, y_test, _ = load_and_prepare(TRAIN, TEST)
    pred = model.predict(X_test)
    assert recall_score(y_test, pred) >= 0.90
    assert precision_score(y_test, pred) >= 0.60


def test_probabilites_valides():
    model = joblib.load("models/xgboost.joblib")
    _, X_test, *_ = load_and_prepare(TRAIN, TEST)
    proba = model.predict_proba(X_test)[:, 1]
    assert ((proba >= 0) & (proba <= 1)).all()


def test_categorie_inconnue_ne_plante_pas():
    model = joblib.load("models/xgboost.joblib")
    _, X_test, *_ = load_and_prepare(TRAIN, TEST)
    ligne = X_test.iloc[[0]].copy()
    ligne[CAT_COLS] = -1
    proba = model.predict_proba(ligne)[0, 1]
    assert 0 <= proba <= 1