import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Elon Tweet 回帰課題 提出アプリ", layout="centered")
st.title("🚀 Elon Musk Tweet 回帰課題：提出＆ランキング")

# 保存先
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 提出フォーム
st.markdown("### 📤 提出フォーム")
name = st.text_input("あなたの名前（例：yamada_taro）")
uploaded_file = st.file_uploader("提出ファイル（CSV形式, actual / predicted 列を含む）", type="csv")

if uploaded_file is not None and name:
    safe_name = name.strip().replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, f"{safe_name}.csv")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ {safe_name}.csv をアップロード・保存しました！")

# リーダーボード作成
st.markdown("### 📊 リーダーボード（MAE昇順）")
results = []
for file_name in os.listdir(UPLOAD_DIR):
    if file_name.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(UPLOAD_DIR, file_name))
            if "actual" in df.columns and "predicted" in df.columns:
                mae = mean_absolute_error(df["actual"], df["predicted"])
                r2 = r2_score(df["actual"], df["predicted"])
                submitter = file_name.replace(".csv", "")
                results.append({"名前": submitter, "MAE": mae, "R²": r2})
        except Exception as e:
            pass

if results:
    leaderboard_df = pd.DataFrame(results)
    leaderboard_df = leaderboard_df.sort_values(by="MAE", ascending=True).reset_index(drop=True)
    leaderboard_df.index += 1
    leaderboard_df["順位"] = leaderboard_df.index

    leaderboard_df.loc[leaderboard_df["順位"] == 1, "順位"] = "🥇 1"
    leaderboard_df.loc[leaderboard_df["順位"] == 2, "順位"] = "🥈 2"
    leaderboard_df.loc[leaderboard_df["順位"] == 3, "順位"] = "🥉 3"

    leaderboard_df = leaderboard_df[["順位", "名前", "MAE", "R²"]]
    st.dataframe(leaderboard_df.style.highlight_min(subset=["MAE"], axis=0, color="lightgreen"))
else:
    st.info("まだ提出ファイルがありません。")