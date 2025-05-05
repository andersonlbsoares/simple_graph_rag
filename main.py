from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tempfile
import os

from core.text_utils import extrair_texto_pdf, extrair_relacoes
from core.neo4j_utils import inserir_relacoes_neo4j, buscar_contexto_neo4j
from core.llm import call_llm

app = Flask(__name__)
CORS(app)

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({"erro": "Arquivo não encontrado na requisição"}), 400

        file = request.files['file']
        filename = secure_filename(file.filename)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        texto = extrair_texto_pdf(tmp_path)
        relacoes = extrair_relacoes(texto)
        inserir_relacoes_neo4j(relacoes)

        os.remove(tmp_path)
        return jsonify({"message": f"{len(relacoes)} relações inseridas com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()
        pergunta = data.get("pergunta")

        if not pergunta:
            return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400

        contexto = buscar_contexto_neo4j(pergunta)
        resposta_contexto = call_llm(pergunta, contexto)
        resposta_sem_contexto = call_llm(pergunta)

        return jsonify({
            "resposta_contexto": resposta_contexto,
            "resposta_sem_contexto": resposta_sem_contexto
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)