from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
from datetime import datetime
import pytz
import os

# טוען את קובץ ה-.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


# שולף את מפתח ה-API מתוך משתני הסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

# יצירת אפליקציית Flask
app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return "Welcome to the Uzi Server!"


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"message": "Use POST to send data to this endpoint."})

    user_input = request.json.get('user_input', '')
    return jsonify({"response": f"You said: {user_input}"})


@app.route('/get_time_info', methods=['GET','POST'])
def get_time_info():
    try:
        # קריאה לנתוני אזור הזמן מהבקשה
        user_timezone = request.json.get('timezone', 'Asia/Jerusalem')  # ברירת מחדל: ירושלים
        tz = pytz.timezone(user_timezone)
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

        # שליחת בקשה ל-OpenAI
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"The current time in {user_timezone} is {current_time}. You are a helpful assistant."},
                {"role": "user", "content": "What can you tell me about the current time?"}
            ]
        )

        # מחזיר את התשובה מהמודל
        return jsonify({"current_time": current_time, "assistant_response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# הפעלת השרת
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
