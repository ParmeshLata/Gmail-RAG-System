import imaplib
import email
import json
import re
import os
from dotenv import load_dotenv

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            if content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")
                    break
            elif content_type == "text/html" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    html = payload.decode(errors="ignore")
                    body = re.sub(r"<[^>]+>", " ", html).strip()
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")
        else:
            body = str(msg.get_payload())
    return body.strip()


def fetch_all_emails(max_emails=500, only_unread=False):
    print("Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    load_dotenv(override=True)
    
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    
    if not EMAIL or not PASSWORD:
        raise ValueError("EMAIL or PASSWORD not found in .env — please save credentials first.")
    
    print(f"Connecting as {EMAIL}...")

    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    if only_unread:
        print("Fetching unread emails...")
        status, messages = mail.uid("search", None, "UNSEEN")
    else:
        try:
            with open("data/last_uid.txt", "r") as f:
                last_uid = f.read().strip()
        except:
            last_uid = ""

        if last_uid:
            print(f"Fetching emails after UID {last_uid}...")
            status, messages = mail.uid("search", None, f"(UID {int(last_uid)+1}:*)")
        else:
            print("First run — fetching all emails...")
            status, messages = mail.uid("search", None, "ALL")

    mail_ids = messages[0].split()

    if not mail_ids:
        print("No new emails found.")
        mail.logout()
        return []

    if last_uid and mail_ids[-1].decode() == last_uid:
        print("No new emails since last run.")
        mail.logout()
        return []

    mail_ids = mail_ids[-max_emails:]
    print(f"Fetching {len(mail_ids)} new emails...")

    all_mails = []

    for i in mail_ids:
        status, msg_data = mail.uid("fetch", i, "(RFC822)")
        if msg_data is None or msg_data[0] is None:
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg.get("subject", "(No Subject)")
        sender  = msg.get("from", "(Unknown)")
        date    = msg.get("date", "(Unknown)")
        body    = get_email_body(msg)

        if not body:
            print(f"Skipping (empty body): {subject}")
            continue

        all_mails.append({
            "from": sender,
            "subject": subject,
            "date": date,
            "body": body,
            "status": "unread" if only_unread else "all"
        })


    if not only_unread and mail_ids:
        latest_uid = mail_ids[-1].decode()
        with open("data/last_uid.txt", "w") as f:
            f.write(latest_uid)
        print(f"Updated last_uid to {latest_uid}")

    mail.logout()

    if not all_mails:
        print("No emails with readable content found.")
        return []

    filename="data/unread_emails.json" if only_unread else "data/emails.json"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            existing_emails = json.load(f)
    except:
        existing_emails = []

    existing_emails.extend(all_mails)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_emails, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_mails)} new emails. Total: {len(existing_emails)}")
    return all_mails