import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_URL", "http://api:8000")
st.set_page_config(page_title="Roadmap AI", layout="wide")
st.title("Product Roadmap AI")

@st.cache_data(ttl=30)
def fetch(path):
    return requests.get(f"{API}{path}").json()

features = pd.DataFrame(fetch("/api/features"))
if features.empty:
    st.warning("Нет фич. Добавьте через API /api/features")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Всего фич", len(features))
c2.metric("В работе", (features.status == "in_progress").sum())
c3.metric("Готово", (features.status == "done").sum())
c4.metric("Backlog", (features.status == "backlog").sum())

st.subheader("Приоритизация RICE")
rice = pd.DataFrame(fetch("/api/prioritize/rice"))
if not rice.empty:
    st.plotly_chart(px.bar(rice.head(15), x="title", y="rice_score",
                           title="Топ-15 по RICE"))

st.subheader("Приоритизация WSJF")
wsjf = pd.DataFrame(fetch("/api/prioritize/wsjf"))
if not wsjf.empty:
    st.plotly_chart(px.bar(wsjf.head(15), x="title", y="wsjf_score",
                           title="Топ-15 по WSJF"))

st.subheader("Kano-матрица")
kano = fetch("/api/prioritize/kano/matrix")
for cat, titles in kano.items():
    if titles:
        st.write(f"**{cat}**: {', '.join(titles[:5])}")

st.subheader("Симуляция релиза")
velocity = st.sidebar.number_input("Средняя velocity (SP/мес)", 10.0, 200.0, 40.0)
std = st.sidebar.number_input("Std velocity", 1.0, 50.0, 8.0)
if st.sidebar.button("Симулировать"):
    r = requests.post(f"{API}/api/simulation/run", json={
        "velocity_mean": velocity, "velocity_std": std,
        "n_simulations": 10000}).json()
    st.session_state["sim"] = r

if "sim" in st.session_state:
    s = st.session_state["sim"]
    a, b, c = st.columns(3)
    a.metric("P50 (дней)", f"{s['p50_days']:.0f}")
    b.metric("P85 (дней)", f"{s['p85_days']:.0f}")
    c.metric("P95 (дней)", f"{s['p95_days']:.0f}")
    hist = s["histogram"]
    st.plotly_chart(px.bar(x=hist["bins"][:-1], y=hist["counts"],
                           labels={"x": "Дней", "y": "Частота"},
                           title="Распределение"))
