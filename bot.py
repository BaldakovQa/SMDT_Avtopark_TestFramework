# bot.py
import os
import time
import requests
import zipfile
from io import BytesIO
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()

# Настройка через переменные окружения
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]  # Personal Access Token с правами repo/workflows
REPO_OWNER = os.environ.get("REPO_OWNER", "BaldakovQa")
REPO_NAME = os.environ.get("REPO_NAME", "SMDT_Avtopark_TestFramework")
WORKFLOW_FILE = os.environ.get("WORKFLOW_FILE", "main.yml")  # имя workflow файла в .github/workflows
REF = os.environ.get("REF", "develop")  # ветка для запуска
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "6"))  # сек между опросами

GITHUB_API = "https://api.github.com"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

async def runtests_ui(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Запрос на запуск UI-тестов отправлен в GitHub Actions...")

    # Отправляем workflow_dispatch
    dispatch_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    data = {"ref": REF, "inputs": {"test_type": "ui"}}
    r = requests.post(dispatch_url, json=data, headers=headers)
    if r.status_code not in (204, 201):
        await update.message.reply_text(f"Не удалось запустить workflow: {r.status_code}\n{r.text}")
        return

    await update.message.reply_text("Workflow запущен. Ожидаю начала run...")

    # Найдём созданный run: poll list-runs и выбрать последний созданный недавно
    runs_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE}/runs"
    run_id = None
    started_at = time.time()
    # ждём появления run
    for _ in range(40):
        rr = requests.get(runs_url, headers=headers)
        if rr.status_code == 200:
            items = rr.json().get("workflow_runs", [])
            if items:
                # Берём самый последний run
                run = items[0]
                run_id = run["id"]
                break
        time.sleep(2)

    if not run_id:
        await update.message.reply_text("Не удалось найти workflow run (тайм-аут).")
        return

    await update.message.reply_text(f"Найден run #{run_id}. Ожидаю завершения...")

    # Ожидаем завершение run
    run_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}"
    while True:
        rrun = requests.get(run_url, headers=headers).json()
        status = rrun.get("status")
        conclusion = rrun.get("conclusion")
        if status == "completed":
            await update.message.reply_text(f"Run завершён: conclusion={conclusion}")
            break
        await update.message.reply_text(f"Статус: {status} (ожидание {POLL_INTERVAL}s)...")
        time.sleep(POLL_INTERVAL)

    # Скачиваем артефакты (если есть)
    artifacts_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{run_id}/artifacts"
    ra = requests.get(artifacts_url, headers=headers).json()
    artifacts = ra.get("artifacts", [])
    if not artifacts:
        await update.message.reply_text("Артефактов не найдено.")
        return

    saved_files = []
    for art in artifacts:
        name = art["name"]
        download_url = art["archive_download_url"]
        rdown = requests.get(download_url, headers=headers, stream=True)
        if rdown.status_code == 200:
            # сохранить и распаковать zip
            dest_dir = Path("artifacts") / str(run_id)
            dest_dir.mkdir(parents=True, exist_ok=True)
            z = zipfile.ZipFile(BytesIO(rdown.content))
            z.extractall(dest_dir)
            # затем отправить все файлы (ограничение Telegram ~50 MB для бота, но документ может быть до 50MB)
            for p in dest_dir.rglob("*"):
                if p.is_file():
                    saved_files.append(p)
        else:
            await update.message.reply_text(f"Ошибка скачивания артефакта {name}: {rdown.status_code}")

    # Отправляем пользователю (первые N файлов, чтобы не перегружать)
    MAX_SEND = 8
    sent = 0
    for fpath in saved_files:
        if sent >= MAX_SEND:
            break
        size = fpath.stat().st_size
        # Telegram file size limit for bot upload: 50 MB (for document)
        if size > 50 * 1024 * 1024:
            await update.message.reply_text(f"Файл {fpath.name} слишком большой ({size} bytes), пропущен.")
            continue
        await update.message.reply_document(open(fpath, "rb"))
        sent += 1

    await update.message.reply_text("Готово — артефакты отправлены (если были).")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Используй /runtests_ui чтобы запустить UI тесты.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("runtests_ui", runtests_ui))
    print("Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()
