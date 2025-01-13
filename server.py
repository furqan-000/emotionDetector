"""
Flask application for emotion detection.
"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Route for detecting emotions in a given text.

    Returns:
        JSON response:
            - Formatted emotion analysis if valid input is provided.
            - Error message for invalid input or exceptions.
    """
    try:
        data = request.json
        text_to_analyze = data.get("text", "")

        if not text_to_analyze.strip():
            return jsonify({"message": "Invalid text! Please try again."}), 400

        result = emotion_detector(text_to_analyze)

        if result["dominant_emotion"] is None:
            return jsonify({"message": "Invalid text! Please try again."}), 400

        response = (
            f"For the given statement, the system response is 'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
            f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

        return jsonify({"response": response})

    except KeyError as error:
        return jsonify({"error": f"Missing key in request: {error}"}), 400
    except TypeError as error:
        return jsonify({"error": f"Invalid input type: {error}"}), 400
    except ValueError as error:
        return jsonify({"error": f"Invalid value: {error}"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)