import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, r2_score

st.title("🔥 PyTorch課題 提出ランキング（アップロード式）")

# 提出ファイル保存用フォルダ
SUB_DIR = "submissions"
os.makedirs(SUB_DIR, exist_ok=True)

# --- ファイルアップロード ---
st.subheader("📤 あなたのCSVファイルをアップロードしてください")
uploaded_file = st.file_uploader("CSVファイルを選択してください（actual, predicted列が必要）", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "actual" in df.columns and "predicted" in df.columns:
            mae = mean_absolute_error(df["actual"], df["predicted"])
            r2 = r2_score(df["actual"], df["predicted"])

            name = st.text_input("お名前（例：yamada_taro）", value="your_name_here")
            save_file = os.path.join(SUB_DIR, f"{name}.csv")

            if st.button("評価して保存・ランキング追加"):
                # ファイルを submissions/ に保存
                df.to_csv(save_file, index=False)
                st.success(f"✅ {name}.csv を保存しました！MAE: {mae:.2f}, R²: {r2:.4f}")
        else:
            st.error("❌ 'actual' と 'predicted' カラムが必要です。")
    except Exception as e:
        st.error(f"⚠️ 読み込みエラー: {e}")

# --- 保存済みファイルからランキング作成 ---
st.subheader("📊 提出済みファイルランキング")
results = []
for file in os.listdir(SUB_DIR):
    if file.endswith(".csv"):
        filepath = os.path.join(SUB_DIR, file)
        try:
            df = pd.read_csv(filepath)
            if "actual" in df.columns and "predicted" in df.columns:
                mae = mean_absolute_error(df["actual"], df["predicted"])
                r2 = r2_score(df["actual"], df["predicted"])
                results.append({
                    "name": file.replace(".csv", ""),
                    "MAE": mae,
                    "R2": r2
                })
        except:
            pass

if results:
    ranking_df = pd.DataFrame(results)
    ranking_df = ranking_df.sort_values(by="MAE", ascending=True).reset_index(drop=True)
    st.dataframe(ranking_df.style.highlight_min(axis=0, color="lightgreen"))
else:
    st.info("まだ提出されたファイルがありません。")