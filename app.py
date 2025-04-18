import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score

st.title("🔥 PyTorch課題 提出ランキング（アップロード式）")

# --- 🔼 ファイルアップロード ---
st.subheader("📤 あなたのCSVファイルをアップロードしてください")
uploaded_file = st.file_uploader("CSVファイルを選択してください（actual, predicted列が必要）", type="csv")

# --- 🧮 ランキング一時保持用 ---
ranking_records = []

# --- 📈 評価 & 追加 ---
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "actual" in df.columns and "predicted" in df.columns:
            mae = mean_absolute_error(df["actual"], df["predicted"])
            r2 = r2_score(df["actual"], df["predicted"])

            name = st.text_input("お名前（例：yamada_taro）", value="your_name_here")
            if st.button("評価してランキングに追加"):
                ranking_records.append({"name": name, "MAE": mae, "R2": r2})
                st.success(f"✅ 評価完了！MAE: {mae:.2f} / R²: {r2:.4f}")
        else:
            st.error("❌ 'actual'と'predicted'列が必要です。")
    except Exception as e:
        st.error(f"⚠️ CSVの読み込みに失敗しました: {e}")

# --- 📊 ランキング表示 ---
if ranking_records:
    result_df = pd.DataFrame(ranking_records)
    result_df = result_df.sort_values(by="MAE", ascending=True).reset_index(drop=True)
    st.subheader("📊 現在のセッション内ランキング")
    st.dataframe(result_df.style.highlight_min(axis=0, color='lightgreen'))