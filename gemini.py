import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY_GEMINI"])


model = genai.GenerativeModel("gemini-1.5-flash")

# Nom du pokemon en français
pokemon = "ss"
request = "Quel est le nom français de ce pokemon : " + pokemon
response = model.generate_content(request)
print(response.text)
