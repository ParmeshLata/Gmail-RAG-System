from config import (system_prompt,API, MODEL)
from rag.retrieval import retrieve_context
from gmail.fetch_emails import fetch_all_emails
from google import genai

UNREAD_TRIGGERS = [
    "unread", "unseen", "not read", "new emails", "new messages",
    "haven't read", "pending emails", "latest emails", "recent emails",
    "any new", "do i have emails", "check my emails"
]

def get_text(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return content[0].get("text", "") if content else ""
    return str(content)


client = genai.Client(api_key=API)


def chatbot(user_prompt, history):

    if any(trigger in user_prompt.lower() for trigger in UNREAD_TRIGGERS):
        unread_emails = fetch_all_emails(only_unread=True)
        if not unread_emails:
            retrieved_context="No new messages found."
        else: 
            results = "\n\n".join([
                f"From: {e['from']}\nSubject: {e['subject']}\nDate: {e['date']}\nBody: {e['body'][:300]}"
                for e in unread_emails
            ])
    else:
        results=retrieve_context(user_prompt)
        if isinstance(results, str):
            retrieved_context = results
        else:
            retrieved_docs = results["documents"][0][:3]
            retrieved_context = "\n\n".join(retrieved_docs)


    formatted_history = []

    formatted_history.append({
        "type": "user_input",
        "content": [{"type": "text", "text": system_prompt}]})
    
    for h in history:
        text=get_text(h["content"])
        if h["role"] == "user":
            formatted_history.append({
                "type": "user_input",
                "content": [{"type": "text", "text": text}]
            })
        else:
            formatted_history.append({
                "type": "model_output",
                "content": [{"type": "text", "text": text}]
            })

    formatted_history.append({
        "type": "user_input",
        "content": [{"type": "text", "text": user_prompt}]
    })


    formatted_history.append({
        "type":"user_input",
        "content":[{"type":"text", "text":f"""Here is the query from the user:\n{user_prompt}
    # Here is additional context that may be relevant:\n{retrieved_context}
    # Important: If the user is referring to something already discussed in the conversation history 
    # (like "2nd one", "that email", "summarize it", "first one" etc.), 
    # always refer back to the conversation history first and IGNORE the additional context.
    # Only use the additional context if the user is asking something new.
    # Reply based on the above instructions."""}]
    })

    print("Prompt Size:", len(str(formatted_history)))

    response = client.interactions.create(
        model=MODEL,
        store=False,
        input=formatted_history
    )
    return response.steps[-1].content[0].text