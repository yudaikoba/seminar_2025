import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Elon Tweet 回帰課題 提出アプリ", layout="centered")
st.title("🚀 Elon Musk Tweet 回帰課題：提出＆ランキング")

# 提出ファイル保存用フォルダ
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# アップロード説明
st.markdown("""
### 📤 提出方法
- `actual`, `predicted` の2列を含む `.csv` をアップロードしてください。
- ファイル名は自動で記録され、精度（MAE / R²）を元にランキング表示されます。
""")

# ファイルアップロード
uploaded_file = st.file_uploader("提出ファイル（CSV形式）をアップロード", type="csv")
if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ ファイル {uploaded_file.name} をアップロードしました！")

# --- リーダーボード作成 ---
st.markdown("### 📊 リーダーボード（MAE昇順）")

results = []
for file_name in os.listdir(UPLOAD_DIR):
    if file_name.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(UPLOAD_DIR, file_name))
            if "actual" in df.columns and "predicted" in df.columns:
                mae = mean_absolute_error(df["actual"], df["predicted"])
                r2 = r2_score(df["actual"], df["predicted"])
                results.append({
                    "ファイル名": file_name,
                    "MAE": mae,
                    "R²": r2
                })
        except:
            pass

# 表示処理
if results:
    leaderboard_df = pd.DataFrame(results)
    leaderboard_df = leaderboard_df.sort_values(by="MAE", ascending=True).reset_index(drop=True)
    leaderboard_df.index += 1
    leaderboard_df["順位"] = leaderboard_df.index

    # メダル付与
    leaderboard_df.loc[leaderboard_df["順位"] == 1, "順位"] = "🥇 1"
    leaderboard_df.loc[leaderboard_df["順位"] == 2, "順位"] = "🥈 2"
    leaderboard_df.loc[leaderboard_df["順位"] == 3, "順位"] = "🥉 3"

    leaderboard_df = leaderboard_df[["順位", "ファイル名", "MAE", "R²"]]
    st.dataframe(leaderboard_df.style.highlight_min(subset=["MAE"], axis=0, color="lightgreen"))
else:
    st.info("まだ提出ファイルがありません。")