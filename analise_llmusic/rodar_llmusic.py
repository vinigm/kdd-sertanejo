import pandas as pd
import requests # Usaremos 'requests' para chamar a API local do Ollama
import json
import time
import random
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
# A biblioteca do Google NÃO é mais necessária aqui

print("--- Iniciando o pipeline LLMusic (Versão Local com Ollama) ---")

# --- 1. Carregar os Dados ---
try:
    df = pd.read_csv("../pre_processamento/musicas_por_trechos_limpo_20251116_112423.csv")
    trechos = df['letra'].dropna().astype(str).tolist()
    print(f"Carregados {len(trechos)} trechos únicos.")
except FileNotFoundError:
    print("Erro: Arquivo não encontrado em '../pre_processamento/musicas_por_trechos_limpo_20251116_112423.csv'")
    exit()

# --- 2. Etapa 1: Geração de Temas (com LLM Local) ---
print("\n--- ETAPA 1: Gerando temas com o LLM (Ollama) ---")
print("Isso vai usar o processamento do seu computador...")

N_ITERACOES = 10
TRECHOS_POR_LOTE = 20
TEMAS_POR_LOTE = 5

lista_de_temas_gerados = []
url_ollama = "http://localhost:11434/api/generate" # API local do Ollama

for i in range(N_ITERACOES):
    print(f"\nIniciando Iteração {i + 1}/{N_ITERACOES}...")
    random.shuffle(trechos)
    lotes = [trechos[j:j + TRECHOS_POR_LOTE] for j in range(0, len(trechos), TRECHOS_POR_LOTE)]
    print(f"Processando {len(lotes)} lotes...")

    for count, lote in enumerate(lotes):
        trechos_formatados = "\n".join([f"{idx+1}. {trecho}" for idx, trecho in enumerate(lote)])
        
        prompt = (
            f"dado os seguintes trechos de música, "
            f"sugira {TEMAS_POR_LOTE} tópicos que descrevem os assuntos abordados:\n\n"
            f"{trechos_formatados}\n\n"
            f"REGRAS:\n"
            f"- Responda APENAS com os tópicos, um por linha.\n"
            f"- Não inclua números na sua resposta.\n"
            f"- Gere temas curtos e conceituais (ex: 'Sofrimento por amor', 'Festa e bebida')."
        )
        
        # Estrutura de dados que o Ollama espera
        data = {
            "model": "llama3:8b", # O modelo que baixamos
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        try:
            # Envia a requisição para a sua máquina local
            response = requests.post(url_ollama, json=data)
            response_json = response.json()
            
            temas = response_json.get('response', '').strip().split('\n')
            lista_de_temas_gerados.extend(temas)
            
            if (count + 1) % 50 == 0:
                print(f"  ...lote {count + 1}/{len(lotes)} processado.")

        except requests.exceptions.ConnectionError:
            print("ERRO DE CONEXÃO: O Ollama não está rodando. Inicie o Ollama e tente novamente.")
            exit()
        except Exception as e:
            print(f"  Erro inesperado no lote {count + 1}: {e}. Pulando.")
            time.sleep(1)

print(f"\n--- Geração de Temas Concluída ---")
print(f"Total de temas gerados: {len(lista_de_temas_gerados)}")

pd.DataFrame(lista_de_temas_gerados, columns=["tema"]).to_csv("temas_gerados_llmusic_local.csv", index=False)

# --- 3. Etapa 2: Agrupamento de Temas (BERTopic) ---
print("\n--- ETAPA 2: Agrupando temas com BERTopic ---")

print("Carregando modelo de embedding...")
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

print("Instanciando o modelo BERTopic...")
topic_model_llmusic = BERTopic(
    embedding_model=embedding_model,
    language="multilingual",
    verbose=True
)

print("Iniciando o treinamento do modelo nos temas gerados...")
topics, probabilities = topic_model_llmusic.fit_transform(lista_de_temas_gerados)

# --- 4. Visualizar os Resultados ---
print("\n--- TÓPICOS ENCONTRADOS (Pipeline LLMusic - Local) ---")
topic_info_llmusic = topic_model_llmusic.get_topic_info()
print(topic_info_llmusic)

topic_info_llmusic.to_csv("resultados_llmusic_pipeline_local.csv", index=False)

print("\n--- Script Concluído ---")