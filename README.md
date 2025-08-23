# Collatz Extension App

拡張コラッツ予想 (3n+q) の挙動を研究するためのWebアプリ。

## 機能
- バックエンド: FastAPI
- 数式処理: SymPy
- テスト: pytest

## 使い方
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
