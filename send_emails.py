# send_emails.py

import csv
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

from settings import settings

COLUMNS = ("account", "login", "email", "key", "note")


def load_recipients(csv_path: Path = settings.CSV_PATH) -> list[dict[str, str]]:
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [h.strip().lower() for h in reader.fieldnames or []]
        missing = [c for c in COLUMNS if c not in reader.fieldnames]
        if missing:
            sys.exit(f"В {csv_path} нет колонок: {', '.join(missing)}")

        recipients, seen = [], set()
        for row in reader:
            row = {c: (row[c] or "").strip() for c in COLUMNS}
            email = row["email"].lower()
            if not email or not row["key"]:
                print(f"  пропуск строки {reader.line_num}: пустой email или key")
                continue
            if email in seen:
                print(f"  пропуск строки {reader.line_num}: дубль {email}")
                continue
            seen.add(email)
            recipients.append(row)
    return recipients


def send_emails(
    send: bool = False,
    csv_path: Path = settings.CSV_PATH,
    template_path: Path = settings.TEMPLATE_PATH,
    subject: str = settings.EMAIL_SUBJECT,
    smtp_host: str = settings.SMTP_HOST,
    smtp_port: int = settings.SMTP_PORT,
    smtp_user: str = settings.SMTP_USER,
    smtp_password: str = settings.SMTP_PASSWORD,
) -> None:
    template = template_path.read_text(encoding="utf-8")
    recipients = load_recipients(csv_path)

    # Проверяем шаблон на каждом получателе до отправки, чтобы не упасть посреди рассылки
    try:
        bodies = [template.format_map(r) for r in recipients]
    except (KeyError, ValueError, IndexError) as e:
        sys.exit(f"Ошибка в шаблоне {template_path}: {type(e).__name__} {e}")

    print(f"\nПолучателей: {len(recipients)}")
    for r in recipients:
        print(f"  {r['email']:<40} {r['login']}")

    if not send:
        print("\nПроверка завершена, письма не отправлялись. Для отправки: --send")
        return

    if not smtp_user or not smtp_password:
        sys.exit("Не заданы SMTP_USER / SMTP_PASSWORD в .env")

    ok, failed = 0, []
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
        smtp.login(smtp_user, smtp_password)
        for r, body in zip(recipients, bodies):
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = r["email"]
            msg.set_content(body)
            try:
                smtp.send_message(msg)
                ok += 1
                print(f"  ✓ {r['email']}")
            except Exception as e:
                # Только тип ошибки — без текста, чтобы не утёк ключ
                failed.append(r["email"])
                print(f"  ✗ {r['email']}: {type(e).__name__}")

    print(f"\nУспешно: {ok}, ошибок: {len(failed)}")
    for email in failed:
        print(f"  не отправлено: {email}")


def main() -> None:
    send = "--send" in sys.argv
    send_emails(send)


if __name__ == "__main__":
    main()
