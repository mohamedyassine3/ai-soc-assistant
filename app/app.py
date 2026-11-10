import os
import sys

import joblib
import pandas as pd
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from preprocess import CAT_COLS

st.set_page_config(page_title="AI SOC Assistant", layout="wide")
st.title("AI-Powered SOC Assistant")
st.caption("Détection d'attaques réseau (UNSW-NB15) par XGBoost")


@st.cache_resource
def load_artifacts():
    model = joblib.load("models/xgboost.joblib")
    enc = joblib.load("models/encoder.joblib")
    return model, enc


@st.cache_data
def load_scored_data():
    model, enc = load_artifacts()
    df = (pd.read_csv("data/UNSW_NB15_testing-set.csv")
          .drop(columns=["id"], errors="ignore")
          .drop_duplicates().reset_index(drop=True))
    X = df.drop(columns=["label", "attack_cat"])
    X[CAT_COLS] = enc.transform(X[CAT_COLS])
    df["proba"] = model.predict_proba(X)[:, 1]
    return df


df = load_scored_data()

seuil = st.sidebar.slider("Seuil de détection", 0.0, 1.0, 0.5, 0.05)
df["alerte"] = (df["proba"] >= seuil).astype(int)

vrais_pos = int(((df["alerte"] == 1) & (df["label"] == 1)).sum())
faux_pos = int(((df["alerte"] == 1) & (df["label"] == 0)).sum())
manquees = int(((df["alerte"] == 0) & (df["label"] == 1)).sum())
nb_alertes = vrais_pos + faux_pos
precision = vrais_pos / nb_alertes if nb_alertes else 0
recall = vrais_pos / (vrais_pos + manquees)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Alertes levées", f"{nb_alertes:,}")
c2.metric("Precision", f"{precision:.2f}")
c3.metric("Recall", f"{recall:.2f}")
c4.metric("Attaques manquées", f"{manquees:,}")

st.subheader("Alertes par catégorie d'attaque")
st.bar_chart(df[df["alerte"] == 1]["attack_cat"].value_counts())

st.subheader("Alertes les plus suspectes")
cols = ["proto", "service", "state", "attack_cat", "proba"]
top = df[df["alerte"] == 1].sort_values("proba", ascending=False).head(50)
st.dataframe(top[cols], use_container_width=True)