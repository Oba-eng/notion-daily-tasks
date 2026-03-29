import os
import requests
from datetime import datetime, timezone, timedelta


# =============================================
# ▼ デイリータスクの内容はここを編集してください ▼
# =============================================
DAILY_TASKS = [
    "メールチェック・返信",
    "ポイント獲得状況の確認",
    "新着案件チェック",
    "明日のタスク整理",
]
# =============================================
# ▲ ここまで（タスクを追加・変更・削除できます）▲
# =============================================


# 設定（変更不要）
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
PROJECT_DB_ID = "264ca961a2ac831f9a6381665a3c48df"
TASK_DB_ID    = "cd2ca961a2ac837f8362813777dc1559"


HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_today_jst():
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).strftime("%Y/%m/%d")


def create_project(date_str):
    """プロジェクトDBにデイリータスクプロジェクトを作成"""
    url = "https://api.notion.com/v1/pages"
    data = {
