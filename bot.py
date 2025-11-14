# bot.py
import os
import time
import requests
import zipfile
from io import BytesIO
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ============================
# Переменные окружения
# ============================

# ИМЕНА ПЕРЕМЕННЫХ: TELEGRAM_TOKEN, GITHUB_TOKEN, REPO_OWNER, REPO_NAME, WORKFLOW_FILE, REF
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPO_OWNER = os.environ.get("REPO_OWNER", "BaldakovQa")
REPO_NAME = os.environ.get("REPO_NAME", "SMDT_Avtopark_TestFramework")
WORKFLOW_FILE = os.environ.get("WORKFLOW_FILE", "run_ui_tests.yml")
REF = os.environ.get("REF", "develop")

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "6"))

GITHUB_API = "https://api.github.com"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}


# ============================
# Команда /runtests_ui
# ============================

async def runtests_ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text("🚀 Отправляю запрос на запуск UI-тестов...")

    dispatch_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"

    data = {"ref": REF, "inputs": {"test_type": "ui"}}

    r = requests.post(dispatch_url, json=data, headers=headers)

    if r.status_code not in (204, 201):
        await update.message.reply_text(f"❌ Ошибка запуска workflow:\n{r.status_code}\n{r.text}")
        return

    await update.message.reply_text("▶ Workflow запущен, ожидаю появления run...")

    # Поиск ID workflow run
    runs_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/runs"

    run_id = None

    for _ in range(40):
        rr = requests.get(runs_url, headers=headers)
        if rr.status_code == 200:
            items = rr.json().get("workflow_runs", [])
            if items:
                run = items[0]
                run_id = run["id"]
                break
        time.sleep(2)

    if not run_id:
        await update.message.reply_text("❌ Не удалось найти workflow run.")
        return

    await update.message.reply_text(f"🔍 Run найден: {run_id}\nОжидаю завершения...")

    # Ждём завершения run
    run_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"

    while True:
        rrun = requests.get(run_url, headers=headers).json()
        status = rrun.get("status")
        conclusion = rrun.get("conclusion")

        if status == "completed":
            await update.message.reply_text(f"✅ Run завершён! Результат: {conclusion}")
            break

        time.sleep(POLL_INTERVAL)

    # Загружаем артефакты
    artifacts_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts"
    ra = requests.get(artifacts_url, headers=headers).json()
    artifacts = ra.get("artifacts", [])

    if not artifacts:
        await update.message.reply_text("⚠ Артефактов нет.")
        return

    await update.message.reply_text("📦 Загружаю артефакты...")

    saved_files = []

    for art in artifacts:
        download_url = art["archive_download_url"]
        rdown = requests.get(download_url, headers=headers, stream=True)

        if rdown.status_code == 200:
            dest_dir = Path("artifacts") / str(run_id)
            dest_dir.mkdir(parents=True, exist_ok=True)

            z = zipfile.ZipFile(BytesIO(rdown.content))
            z.extractall(dest_dir)

            for p in dest_dir.rglob("*"):
                if p.is_file():
                    saved_files.append(p)

    # Отправляем в Telegram
    MAX_SEND = 8
    sent = 0

    for fpath in saved_files:
        if sent >= MAX_SEND:
            break
        if fpath.stat().st_size < 50 * 1024 * 1024:
            await update.message.reply_document(open(fpath, "rb"))
            sent += 1

    await update.message.reply_text("🎉 Готово! Артефакты отправлены.")


# ============================
# Команда /start
# ============================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Используй команду /runtests_ui для запуска тестов.")


# ============================
# MAIN
# ============================

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("runtests_ui", runtests_ui))

    print("Bot started!")
    app.run_polling()


if __name__ == "__main__":
    main()
