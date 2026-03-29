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
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": PROJECT_DB_ID},
        "properties": {
            "プロジェクト": {"title": [{"text": {"content": f"デイリータスク - {date_str}"}}]},
            "ステータス": {"status": {"name": "計画中"}},
            "案件種類": {"multi_select": [{"name": "日時タスク"}]},
        },
    }
    res = requests.post(url, headers=HEADERS, json=data)
    res.raise_for_status()
    page = res.json()
    print(f"✅ プロジェクト作成: {page['url']}")
    return page["id"]

def create_task(task_name, project_page_id):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": TASK_DB_ID},
        "properties": {
            "タスク": {"title": [{"text": {"content": task_name}}]},
            "ステータス": {"status": {"name": "未着手"}},
            "案件の種類": {"relation": [{"id": project_page_id}]},
        },
    }
    res = requests.post(url, headers=HEADERS, json=data)
    res.raise_for_status()
    print(f"  📝 タスク作成: {task_name}")

def main():
    date_str = get_today_jst()
    print(f"🗓️  {date_str} のデイリータスクを作成します...")
    project_id = create_project(date_str)
    for task in DAILY_TASKS:
        create_task(task, project_id)
    print(f"\n🎉 完了！{len(DAILY_TASKS)}件のタスクを作成しました")

if __name__ == "__main__":
    main()
