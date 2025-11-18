import pandas as pd
import re
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

print("--- Iniciando Refinamento de Tópicos ---")

# --- 1. Carregar os dados brutos (A Matéria-Prima) ---
arquivo_entrada = "temas_gerados_llmusic_local.csv"
arquivo_saida = "resultados_llmusic_refinado_final.csv" # NOME DO NOVO ARQUIVO

try:
    print(f"Lendo arquivo original: {arquivo_entrada}...")
    df = pd.read_csv(arquivo_entrada)
    # Garante que estamos pegando todas as linhas, convertendo para string
    temas_brutos = df['tema'].dropna().astype(str).tolist()
    print(f"-> Total de temas brutos carregados: {len(temas_brutos)}")
except FileNotFoundError:
    print(f"ERRO: Não encontrei o arquivo '{arquivo_entrada}'. Verifique a pasta.")
    exit()

# --- 2. Função de Limpeza (Sua camada extra de PLN) ---
def limpar_tema(texto):
    # 1. Remove numeração inicial (ex: "1. ", "2-")
    texto = re.sub(r'^\d+[\.\-\)]\s*', '', texto)
    # 2. Remove marcadores (bullets) (ex: "•", "*", "-")
    texto = re.sub(r'^[\•\*\-\>]\s*', '', texto)
    # 3. Remove pontuação excessiva no final ou início
    texto = texto.strip(".,:;!?'\" ")
    # 4. Converte para minúsculas para padronizar
    return texto.lower()

print("\nAplicando limpeza nos textos...")
temas_limpos = [limpar_tema(t) for t in temas_brutos]

# --- 3. Filtragem de "Lixo" do LLM ---
# Removemos linhas vazias ou frases que são conversa do chatbot, não tópicos
print("Filtrando frases inúteis (lixo do LLM)...")
termos_lixo = [
    "aqui estao", "aqui están", "here are", "sugiro", "topicos sugeridos", 
    "temas abordados", "seguintes topicos", "describe the subjects",
    "topic suggestions", "lista de topicos", "assuntos abordados",
    "descrevem os assuntos", "tópicos que descrevem", "cinco tópicos",
    "5 tópicos", "futebol"  # Remove o tópico "futebol" que apareceu vazio
]

temas_filtrados = []
temas_removidos = []
for tema in temas_limpos:
    # Só aceita se tiver mais de 3 letras, NÃO tiver termos de lixo e não for vazio/muito curto
    if len(tema) > 5 and not any(lixo in tema for lixo in termos_lixo) and tema.strip():
        temas_filtrados.append(tema)
    else:
        temas_removidos.append(tema)

print(f"-> Temas válidos após limpeza: {len(temas_filtrados)} (de {len(temas_brutos)})")
print(f"-> Temas removidos como lixo: {len(temas_removidos)}")
print(f"\nExemplos de lixo removido (primeiros 10):")
for exemplo in temas_removidos[:10]:
    print(f"  - '{exemplo}'")

# --- 4. Re-Agrupamento com BERTopic ---
# Agora rodamos o modelo na lista limpa. Ele vai agrupar "sofrimento" com "sofrimento"
# e somar automaticamente na coluna 'Count'.
print("\nRe-calculando tópicos e contagens com BERTopic...")

embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
# min_topic_size maior ajuda a evitar micro-tópicos repetidos
topic_model = BERTopic(
    embedding_model=embedding_model, 
    language="multilingual", 
    min_topic_size=15, 
    verbose=True
)

topics, probs = topic_model.fit_transform(temas_filtrados)
topic_info = topic_model.get_topic_info()

# --- 5. Salvar o NOVO arquivo ---
print(f"\nSalvando resultados em: {arquivo_saida}")
topic_info.to_csv(arquivo_saida, index=False)

print("\n--- AMOSTRA DOS TOP 10 TÓPICOS CONSOLIDADOS ---")
print(topic_info[['Topic', 'Count', 'Name']].head(11))

print("\n--- ESTATÍSTICAS FINAIS ---")
print(f"Total de tópicos encontrados: {len(topic_info)}")
outliers = topic_info[topic_info['Topic'] == -1]['Count'].sum() if -1 in topic_info['Topic'].values else 0
print(f"Temas classificados como outliers (Topic -1): {outliers}")
print(f"Temas em tópicos válidos: {len(temas_filtrados) - outliers}")
print(f"\nArquivo salvo: {arquivo_saida}")