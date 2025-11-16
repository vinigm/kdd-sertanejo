import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
# Importação necessária para stopwords
from sklearn.feature_extraction.text import CountVectorizer 

print("--- Iniciando o pipeline BERTopic (com Stopwords) ---")

# --- 1. Carregar os Dados ---
try:
    # Carrega o dataset de trechos pré-processados
    df = pd.read_csv("../pre_processamento/musicas_por_trechos_limpo_20251116_112423.csv")
    
    # Usa a coluna 'letra' que contém os trechos das músicas
    trechos = df['letra'].dropna().astype(str).tolist()
    
    print(f"Carregados {len(trechos)} trechos únicos.")
    print(f"Exemplo do primeiro trecho: {trechos[0]}")
except FileNotFoundError:
    print("Erro: Arquivo CSV não encontrado.")
    print("Verifique se o arquivo está em '../pre_processamento/musicas_por_trechos_limpo_20251116_112423.csv'")
    exit()
except KeyError:
    print("Erro: A coluna 'letra' não foi encontrada no CSV.")
    print("Colunas disponíveis:", df.columns.tolist())
    exit()
except Exception as e:
    print(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
    exit()

# --- 2. Configurar o Modelo de Embedding ---
print("Carregando modelo de embedding (isso pode levar um momento)...")
# Este é um bom modelo multilíngue que entende bem o português.
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# --- 3. Definir Stopwords e Vectorizer ---
print("Configurando o Vectorizer com stopwords...")

# Lista de interjeições e "lixo" que você identificou no Tópico 13
interjeicoes = [
    'oh', 'uou', 'ah', 'ooh', 'uô', 'oi', 'iê', 'ha', 'eh', 'uôu', 
    'nanana', 'ererê', 'uh', 'hmm', 'hey', 'laia'
]

# Stopwords comuns do português (incluindo as vistas no Tópico -1)
stopwords_pt = [
        'ser','sou','é','era','foi','estou','tô','ta','tá','tava','estar','vamos','vou','ia','ir','ver','vi','vendo', 'tipo',
        'dizer','disse','fala','falar','falou','diz','quer','querer','quero','pode','poder','podia','deve','dever', 'qual', 'está',
        'tem','têm','tenho','tinha','ter','ficar','fica','ficou','ficando','deixar','deixa','deixou', 'nóis', 'eu', 'demais', 'alguém',
        'pra','pro','pros','q','pq','porque','que','se','me','te','lhe','ela','ele','elas','eles','cê','você','vocês','tb', 'oi',
        'iê','ê','ô','ah','oh','ei','uai','oxe','porra','pá','opa','oba','aê','ae','yeah','la','lá', 'aí', 'ai', 'não', 'todo',
        'a','o','as','os','de','do','da','dos','das','em','no','na','nos','nas','por','para','com','sem','sobre','entre'
]

# Combinar as duas listas (usando 'set' para garantir palavras únicas)
lista_final_stopwords = list(set(interjeicoes + stopwords_pt))

# Criar um modelo de vetorização que USA essa lista de stopwords
# min_df=2 significa que a palavra deve aparecer em pelo menos 2 documentos
# para ser considerada parte da representação do tópico.
vectorizer_model = CountVectorizer(stop_words=lista_final_stopwords, min_df=2)


# --- 4. Instanciar e Treinar o BERTopic ---
print("Instanciando o modelo BERTopic...")
topic_model = BERTopic(
    embedding_model=embedding_model,
    language="multilingual",    # Ajuda o modelo a processar melhor o português
    verbose=True,               # Mostra o progresso
    vectorizer_model=vectorizer_model # Passa o vectorizer customizado
)

print("Iniciando o treinamento do modelo... (Isso pode levar vários minutos)")
topics, probabilities = topic_model.fit_transform(trechos)

# --- 5. Visualizar os Resultados ---
print("\n--- TÓPICOS ENCONTRADOS (BERTopic com Stopwords) ---")
topic_info = topic_model.get_topic_info()
print(topic_info)

# Salva os resultados para análise posterior
topic_info.to_csv("resultados_bertopic_com_stopwords.csv", index=False)

print("\n--- Detalhes dos 5 Tópicos Mais Frequentes ---")
# Mostra as palavras-chave dos 5 tópicos principais (sem contar o -1, que são outliers)
# Usamos [1:6] para pular o tópico -1 (outliers)
for topic_id in topic_info['Topic'].unique()[1:6]: 
    if topic_id in topic_model.get_topics():
        print(f"\n[ Tópico {topic_id} ]")
        # Pega as 10 palavras principais para esse tópico
        print(topic_model.get_topic(topic_id)) 
    else:
        print(f"\n[ Tópico {topic_id} não encontrado após filtragem ]")

print("\n--- Script Concluído ---")