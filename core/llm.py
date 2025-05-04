import requests
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

try:
    client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Erro ao configurar Google Gemini: {e}")
    client = None

def call_llm(pergunta: str, contexto: str = "", model_name: str = "gemini-1.5-flash") -> str:
	try:
		prompt = (
			f"Use o contexto abaixo para responder à pergunta de forma clara e direta.\n\n"
			f"Contexto:\n{contexto}\n\n"
			if contexto else ""
		) + f"Pergunta:\n{pergunta}\n\nResposta:\n"

		response = client.models.generate_content(
			model=model_name,
			contents=prompt,
		)
		return response.text.strip()

	except requests.exceptions.RequestException as e:
		return f"Erro: Falha na comunicação com a API. Detalhes: {e}"
	except Exception as e:
		print(f"Erro inesperado ao chamar LLM: {e}")
		import traceback
		traceback.print_exc()
		return f"Erro inesperado ao processar a chamada LLM. Detalhes: {e}"
