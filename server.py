"""
This is a Flask application that shows us an API endpoint for emotion detection.
It listens for POST requests at the '/emotionDetector' route and expects a 
JSON payload with a 'text' key. The system uses an emotion detection model 
to analyze the text and returns the detected emotions as a response.

Dependencies:
- Flask
- EmotionDetection 

The response includes emotion values for anger, disgust, fear, joy, and sadness,
as well as the dominant emotion which is what we are looking for.
"""
from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

# Initialize the Flask application
app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Handles the /emotionDetector route. It takes a POST request containing a
    JSON payload with the key 'text', processes it to detect emotions, and 
    returns the results as a JSON response.

    Parameters:
        None

    Returns:
        JSON: A response containing the emotion analysis or error message
    """
    try:
        # Retrieve the JSON data from the request
        data = request.json

        # Check if the required 'text' field exists and is not empty
        if not data or 'text' not in data or not data['text'].strip():
            return jsonify({"message": "Invalid text! Try again!"}), 400
        text_to_analyze = data['text']
        result = emotion_detector(text_to_analyze)
        if result['dominant_emotion'] is None:
            return jsonify({"response": "Invalid text! Please try again!"}), 400

        # Prepare the formatted response with emotion values
        dominant_emotion = result['dominant_emotion']
        response = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. The dominant emotion is {dominant_emotion}."
        )
        # Return analysis response
        return jsonify({"response": response})

    except KeyError as error:
        return jsonify({"error": f"Missing key in request: {error}"}), 400
    except TypeError as error:
        return jsonify({"error": f"Invalid input type: {error}"}), 400
    except ValueError as error:
        return jsonify({"error": f"Invalid value: {error}"}), 400

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True, host="0.0.0.0", port=5000)
