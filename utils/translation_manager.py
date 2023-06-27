# File: /cherryAI/utils/translation_manager.py

from google.cloud import translate_v2 as translate

GOOGLE_TRANSLATE_API_KEY = 'AIzaSyDmpdclrQcPjb6sV8yHIgrOlRLiF-PofeI'

def translate_text(text, target_language):
    """
    Translates a given text into the target language using Google's Translation API.

    Parameters:
    text (str): The text to translate.
    target_language (str): The language to translate the text into.

    Returns:
    str: The translated text, or None if the translation failed.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
