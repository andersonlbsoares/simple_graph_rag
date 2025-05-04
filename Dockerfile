# Usar uma imagem base do Python
FROM python:3.10

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para a construção de pacotes Python
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libhdf5-dev \
    python3-dev \
    gfortran \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .
# Instalar as dependências restantes
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir google-generativeai
RUN python -m spacy download pt_core_news_sm

# Copiar o restante dos arquivos para o contêiner
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "main.py"]
