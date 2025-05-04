import spacy
import fitz  # PyMuPDF

# Carregar modelo spaCy
nlp = spacy.load("pt_core_news_sm")

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

def extrair_relacoes(texto):
    relacoes = []
    doc = nlp(texto)

    for sent in doc.sents:
        ents = [ent.text for ent in sent.ents]
        if len(ents) >= 2:
            sujeito = ents[0]
            objeto = ents[1]
            relacao = sent.root.lemma_  # Verbo principal da frase
            relacoes.append((sujeito, relacao, objeto))

    return relacoes