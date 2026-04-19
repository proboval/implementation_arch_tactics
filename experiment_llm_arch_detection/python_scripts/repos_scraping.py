import csv
import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

INPUT_CSV = "dataset_normalized.csv"   # или dataset.csv
OUTPUT_CSV = "dataset_with_commits.csv"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def get_latest_commit_hash(repo_full_name, max_retries=3, base_sleep=1):
    """
    Получает hash последнего коммита default branch репозитория GitHub.
    """
    repo_full_name = (repo_full_name or "").strip()
    if not repo_full_name or "/" not in repo_full_name:
        return ""

    url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=1"

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)

            if response.status_code == 404:
                print(f"[404] Не найден репозиторий: {repo_full_name}")
                return ""

            if response.status_code == 403:
                remaining = response.headers.get("X-RateLimit-Remaining")
                reset_ts = response.headers.get("X-RateLimit-Reset")

                if remaining == "0" and reset_ts:
                    wait_time = max(int(reset_ts) - int(time.time()) + 5, 5)
                    print(f"[RATE LIMIT] Ждём {wait_time} сек. для {repo_full_name}")
                    time.sleep(wait_time)
                    continue

            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                return data[0].get("sha", "")

            print(f"[WARN] Нет коммитов у репозитория: {repo_full_name}")
            return ""

        except requests.RequestException as e:
            print(f"[ERROR] {repo_full_name}, попытка {attempt}/{max_retries}: {e}")
            if attempt < max_retries:
                time.sleep(base_sleep * attempt)
            else:
                return ""

    return ""


def main():
    rows = []

    # Читаем CSV как есть
    with open(INPUT_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        original_fieldnames = reader.fieldnames

        if not original_fieldnames:
            raise ValueError("Не удалось прочитать заголовки CSV.")

        # Определяем колонку с именем репозитория
        if "repo_full_name" in original_fieldnames:
            repo_col = "repo_full_name"
        elif "full_name" in original_fieldnames:
            repo_col = "full_name"
        else:
            raise ValueError("В CSV нет колонки 'repo_full_name' или 'full_name'.")

        # Добавляем commit_hash в конец, если его ещё нет
        if "commit_hash" in original_fieldnames:
            fieldnames = original_fieldnames[:]
        else:
            fieldnames = original_fieldnames[:] + ["commit_hash"]

        for row in reader:
            rows.append(row)

    total = len(rows)
    print(f"Загружено строк: {total}")

    for i, row in enumerate(rows, start=1):
        repo_name = (row.get(repo_col) or "").strip()
        existing_hash = (row.get("commit_hash") or "").strip()

        if existing_hash:
            print(f"[{i}/{total}] Уже есть commit_hash: {repo_name}")
            continue

        print(f"[{i}/{total}] Получаю commit hash для {repo_name}...")
        commit_hash = get_latest_commit_hash(repo_name)
        row["commit_hash"] = commit_hash

        if commit_hash:
            print(f"    -> {commit_hash}")
        else:
            print("    -> не удалось получить")

        time.sleep(0.3)

    # Записываем CSV аккуратно, сохраняя порядок колонок
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        for row in rows:
            # гарантируем наличие всех колонок
            normalized_row = {col: row.get(col, "") for col in fieldnames}
            writer.writerow(normalized_row)

    print(f"\nГотово. Результат сохранён в: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
