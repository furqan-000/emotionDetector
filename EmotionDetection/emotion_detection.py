import requests

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
        }

    input_json = {
        "raw_document": {
            "text": text_to_analyze
            }
        }

    # Check for empty text
    if not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    try:
        # Make the request
        response = requests.post(url, headers=headers, json=input_json)
        
        # Handle invalid responses
        if response.status_code == 400:  # Handle invalid text input
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }
        # Parse the response
        if response.status_code == 200:
            response_data = response.json()
            emotions = response_data.get('emotionPredictions', [{}])[0].get('emotion', {})
            anger = emotions.get('anger', 0)
            disgust = emotions.get('disgust', 0)
            fear = emotions.get('fear', 0)
            joy = emotions.get('joy', 0)
            sadness = emotions.get('sadness', 0)

            # Determine dominant emotion
            emotion_scores = {
                "anger": anger,
                "disgust": disgust,
                "fear": fear,
                "joy": joy,
                "sadness": sadness
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            return {
                "anger": anger,
                "disgust": disgust,
                "fear": fear,
                "joy": joy,
                "sadness": sadness,
                "dominant_emotion": dominant_emotion
            }
        else:
            return {"error": f"Error: {response.status_code}, {response.text}"}
    except Exception as e:
        return {"error": str(e)}