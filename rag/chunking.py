from rag.splitter import split_text
import uuid
import json

def create_email_chunks(emails):

    CHUNKSIZE=1000
    OVERLAP=200

    all_chunks=[]

    for email_idx, mail in enumerate(emails):
        sender=mail.get("from", "")
        date=mail.get("date", "")
        subject=mail.get("subject", "")
        body=mail.get("body", "")

        formated_mail=f"""
        Sender={sender}
        Date={date}
        Subject={subject}
        {body}""".strip()

        text_chunks=split_text(formated_mail, chunk_size=CHUNKSIZE, overlap=OVERLAP)
        total_chunks=len(text_chunks)

        for idx, chunk in enumerate(text_chunks):
            chunk_data={
                "chunk_id":str(uuid.uuid4()),
                "text":chunk,
                "metadata":{
                    "from":sender,
                    "date":date,
                    "subject":subject,
                    "email_index":email_idx,
                    "chunk_index":idx,
                    "total_chunks":total_chunks
                }
            }
            all_chunks.append(chunk_data)

    try:
        with open("data/email_chunks.json", "r", encoding="utf-8") as f:
            existing_chunks = json.load(f)
    except:
        existing_chunks = []

    existing_chunks.extend(all_chunks)

    with open("data/email_chunks.json", "w", encoding="utf-8") as f:
        json.dump(existing_chunks, f, ensure_ascii=False, indent=2)

    print(f"Created {len(all_chunks)} chunks")
    return all_chunks