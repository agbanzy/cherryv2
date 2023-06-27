# File: /cherryAI/dialogflow.py

from google.cloud import dialogflow

def detect_intent(project_id, session_id, text, language_code='en'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text

def detect_intent_texts(project_id, session_id, texts, language_code='en'):
    results = []
    for text in texts:
        result = detect_intent(project_id, session_id, text, language_code)
        results.append(result)
    return results

