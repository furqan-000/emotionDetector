import requests

def emotion_detector (text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }

    input_json = {
        "raw_document": { 
            "text": text_to_analyze 
        }
    }

    if not text_to_analyze.strip():
        return {
            "anger" :  None,
            "disgust" :  None,
            "fear" :  None,
            "joy" :  None,
            "sadness" :  None,
            "dominant_emotion" :  None,
        }

    try: 
        # This starts the code off by making a request
        response = requests.post(url, headers=headers, json=input_json)
        
        # Checks for invalid responses
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"

        response_data = response.json()
        emotion_data = response_data.get('emotionPredictions', [{}])[0].get('emotion', {})

        # It will take the emotion score or set the default to 0
        anger = emotion_data.get('anger', 0)
        disgust = emotion_data.get('disgust', 0)
        fear = emotion_data.get('fear', 0)
        joy = emotion_data.get('joy', 0)
        sadness = emotion_data.get('sadness', 0)
        
        emotion_scores = {
            "anger": anger,
            "disgust": disgust,
            "fear": fear,
            "joy": joy,
            "sadness": sadness,
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

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e: 
        return {"error": f"Unexpected error: {str(e)}"}