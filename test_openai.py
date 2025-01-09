import openai
from dotenv import load_dotenv
from datetime import datetime
from dateutil.parser import parse # type: ignore
import pytz
import os

# טוען את קובץ ה-.env
load_dotenv(dotenv_path="P:/Uzi/Env/.env")

# שולף את מפתח ה-API מתוך משתני הסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

tz = pytz.timezone('Asia/Jerusalem')
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# בדיקה שהמפתח נטען כראוי
if not openai.api_key:
    raise ValueError("API key not found. Make sure it's defined in the .env file and the file is correctly loaded.")

# בקשה לדוגמה ל-OpenAI
response = openai.chat.completions.create(
    model="gpt-4o",  # דגם ה-API שבו תשתמש
    messages=[
         {"role": "system", "content": f"The current time is {current_time}. You are a helpful assistant."},
        {"role": "user", "content": "What can you tell me about the current time?"}
    ]
)

# הדפסת התשובה מהמודל
print(response.choices[0].message.content)
