import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, storage
import uuid

# 🔑 Firebase初期化（初回のみ）
if not firebase_admin._apps:
    cred = credentials.Certificate("./seminar-pytorch-2025-firebase-adminsdk-fbsvc-4b5bcba4e8.json")  # ダウンロードした鍵
    firebase_admin.initialize_app(cred, {
        "storageBucket": "seminar-pytorch-2025"
    })

bucket = storage.bucket()

# アップロード
st.title("📤 PyTorch課題 提出フォーム（Firebase版）")
uploaded_file = st.file_uploader("CSVファイルをアップロード（actual, predicted）", type="csv")

name = st.text_input("あなたの名前（半角英小文字）")

if uploaded_file is not None and name:
    blob_name = f"{name}_{uuid.uuid4()}.csv"
    blob = bucket.blob(blob_name)
    blob.upload_from_file(uploaded_file, content_type="text/csv")
    st.success(f"✅ {blob_name} を保存しました！")