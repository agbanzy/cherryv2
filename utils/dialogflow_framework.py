# File: /cherryAI/utils/dialogflow_framework.py

from dialogflow import detect_intent

def detect_intent_texts(project_id, session_id, texts, language_code='en'):
    results = []
    for text in texts:
        result = detect_intent(project_id, session_id, text, language_code)
        results.append(result)
    return results
