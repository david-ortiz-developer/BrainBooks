from openai import OpenAI
import os
from dotenv import load_dotenv


def get_response(prompt):
    if TESTING_MODE:
        # Respuesta mockeada
        mock_response = {
            "choices": [{
                "message": {
                    "content": "¡Mock: Todo funciona, rockero! 🎸",
                    "role": "assistant"
                }
            }],
            "usage": {"total_tokens": 10}
        }
        return mock_response
    else:
        # Llamada real a la API
        response = client.chat.completions.create(
            model="grok-3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response

TESTING_MODE = True
client = OpenAI(api_key=os.getenv("XAI_API_KEY"))
response = get_response("Hola, ¿funciona?")
print(response.choices[0].message.content)




