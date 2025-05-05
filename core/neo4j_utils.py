
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print(f"Conectando ao Neo4j em {NEO4J_URI} com usuário {NEO4J_USER}")

def inserir_relacoes_neo4j(relacoes):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        for sujeito, relacao, objeto in relacoes:
            session.run("""
                MERGE (a:Entidade {nome: $sujeito})
                MERGE (b:Entidade {nome: $objeto})
                MERGE (a)-[r:RELACAO {tipo: $relacao}]->(b)
            """, sujeito=sujeito, relacao=relacao, objeto=objeto)

    driver.close()

def buscar_contexto_neo4j(pergunta: str) -> str:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    palavras_chave = pergunta.split()
    contexto = ""

    with driver.session() as session:
        for palavra in palavras_chave:
            query = """
				MATCH (a)-[r]->(b)
				WHERE toLower(b.nome) CONTAINS toLower($palavra) 
					OR toLower(a.nome) CONTAINS toLower($palavra)
				RETURN a.nome AS origem, r.tipo AS relacao, b.nome AS destino
				LIMIT 5
			"""
            resultados = session.run(query, palavra=palavra)
            for record in resultados:
                origem = record["origem"]
                relacao = record["relacao"]
                destino = record["destino"]
                contexto += f"- {origem} {relacao} {destino}.\n"
    return contexto