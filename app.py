import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, r2_score

st.title("🔥 PyTorch課題 提出ランキング")
st.markdown("各自の予測精度（MAE, R²）を集計し、ランキング形式で表示します。")

# --- 📂 submissions フォルダからランキング作成 ---
sub_dir = "submissions"
results = []

if os.path.exists(sub_dir):
    for file in os.listdir(sub_dir):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(sub_dir, file))
            if "actual" in df.columns and "predicted" in df.columns:
                mae = mean_absolute_error(df["actual"], df["predicted"])
                r2 = r2_score(df["actual"], df["predicted"])
                results.append({"name": name, "MAE": mae, "R2": r2})

# --- 📊 ランキング表示 ---
if results:
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(by="MAE", ascending=True).reset_index(drop=True)
    st.subheader("📈 現在の提出ランキング")
    st.dataframe(result_df.style.highlight_min(axis=0, color='lightgreen'))
else:
    st.info("まだ submissions/ フォルダに提出ファイルがありません。")

# --- 🆕 CSVアップロード機能 ---
st.subheader("📤 CSVファイルをアップロードして評価する")

uploaded_file = st.file_uploader("提出ファイル（.csv, actual/predicted列を含む）をアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "actual" in df.columns and "predicted" in df.columns:
            mae = mean_absolute_error(df["actual"], df["predicted"])
            r2 = r2_score(df["actual"], df["predicted"])
            st.success("✅ ファイルを読み込みました！")
            st.write(f"**MAE:** {mae:.2f}")
            st.write(f"**R²:** {r2:.4f}")
        else:
            st.error("❌ `actual` と `predicted` カラムが必要です。")
    except Exception as e:
        st.error(f"読み込みエラー：{e}")