from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    # Send the message to Rasa
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'  # Change if your Rasa is hosted elsewhere
    payload = {
        'sender': 'user',  # you can use session ID or username here
        'message': user_message
    }

    try:
        response = requests.post(rasa_url, json=payload)
        bot_response = response.json()

        # Extract the message(s) from Rasa's response
        messages = [msg.get("text", "") for msg in bot_response]
        final_response = ' '.join(messages) if messages else "Sorry, I didn't get that."

    except Exception as e:
        final_response = f"Error contacting Rasa server: {str(e)}"

    return jsonify({'response': final_response})

if __name__ == '__main__':
    app.run(debug=True)
