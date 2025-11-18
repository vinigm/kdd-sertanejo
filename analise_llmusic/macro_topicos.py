import pandas as pd
import requests
import time
import numpy as np
from statistics import mode, StatisticsError

print("--- ETAPA 2: Classificação com Autoconsistência (LLMusic) ---")

# --- 1. CONFIGURAÇÃO ---
ARQUIVO_TRECHOS = "../pre_processamento/musicas_por_trechos_limpo_20251116_112423.csv"
ARQUIVO_SAIDA = "resultado_classificacao_autoconsistencia.csv"

# Definindo os Macro-Tópicos (Baseado na sua análise e na Dissertação)
TOPICOS_ALVO = {
    1: "Romance e Relacionamentos",
    2: "Vida no Crime e Violência",
    3: "Festa, Dança e Diversão",
    4: "Ostentação e Luxo",
    5: "Sofrimento, Saudade e Melancolia",
    6: "Sexualidade e Sedução",
    7: "Família e Maternidade",
    8: "Superação e Fé"
}

N_INFERENCIAS = 5  # O paper usa 10. Para teste local rápido, use 5. Para final, use 10.
TEMPERATURAS = [0.1, 0.4, 0.7, 0.9, 1.0] # Variação para testar robustez (se N=5)

# --- 2. CARREGAR DADOS ---
try:
    # Vamos pegar uma AMOSTRA para não demorar dias rodando localmente
    df = pd.read_csv(ARQUIVO_TRECHOS)
    # PEGA APENAS 50 TRECHOS ALEATÓRIOS PARA TESTE INICIAL
    df_amostra = df.sample(50, random_state=42).reset_index(drop=True) 
    trechos = df_amostra['letra'].astype(str).tolist()
    ids_originais = df_amostra.index.tolist() # Ou use uma coluna de ID se tiver
    print(f"Carregados {len(trechos)} trechos para classificação.")
except FileNotFoundError:
    print("Erro: Arquivo de trechos não encontrado.")
    exit()

# --- 3. FUNÇÃO DE INFERÊNCIA ---
def classificar_trecho(trecho, topico, temperatura):
    url = "http://localhost:11434/api/generate"
    
    # Prompt Zero-Shot conforme Dissertação (Escala 1-5)
    prompt = (
        f"Avaliação da Relação Semântica.\n"
        f"Tópico: {topico}\n"
        f"Trecho: \"{trecho}\"\n\n"
        f"Classifique a relação entre o trecho e o tópico na escala:\n"
        f"1: Nenhuma relação.\n"
        f"2: Relação fraca.\n"
        f"3: Relação moderada.\n"
        f"4: Relação forte.\n"
        f"5: Relação muito forte.\n\n"
        f"Responda EXCLUSIVAMENTE com um único número (1, 2, 3, 4 ou 5)."
    )

    data = {
        "model": "llama3:8b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperatura, "num_predict": 5} # num_predict baixo para forçar resposta curta
    }

    try:
        response = requests.post(url, json=data)
        texto_resp = response.json().get('response', '').strip()
        # Tenta extrair o primeiro número que aparecer
        import re
        match = re.search(r'[1-5]', texto_resp)
        if match:
            return int(match.group(0))
        else:
            return None # Falha na formatação
    except:
        return None

# --- 4. LOOP PRINCIPAL (Self-Consistency) ---
resultados = []

print(f"\nIniciando classificação de {len(trechos)} trechos contra {len(TOPICOS_ALVO)} tópicos...")
print(f"Total de chamadas ao LLM estimadas: {len(trechos) * len(TOPICOS_ALVO) * N_INFERENCIAS}")

start_time = time.time()

for i, trecho in enumerate(trechos):
    print(f"\nProcessando Trecho {i+1}/{len(trechos)}...")
    
    for id_topico, nome_topico in TOPICOS_ALVO.items():
        scores = []
        print(f"  Tópico: {nome_topico}...", end=" ")
        
        # Autoconsistência: Loop de Inferências
        for k in range(N_INFERENCIAS):
            temp = TEMPERATURAS[k % len(TEMPERATURAS)] # Cicla entre as temperaturas
            score = classificar_trecho(trecho, nome_topico, temp)
            if score:
                scores.append(score)
            else:
                print("!", end="")  # Indica falha
            # Pequena pausa para não travar a máquina
            time.sleep(0.1)
        print(f" [{len(scores)}/{N_INFERENCIAS} válidos]") 
        
        # Cálculo das Métricas de Consistência
        if scores:
            media = np.mean(scores)
            try:
                moda = mode(scores)
            except StatisticsError:
                # Se não há moda única, usa mediana (mais robusta que média para empates)
                moda = int(np.median(scores))
            
            desvio = np.std(scores)
            
            # Critério do Paper: Considera Positivo se Moda >= 4
            # Adiciona critério de confiança: desvio baixo indica maior consenso
            classificacao_final = 1 if (moda >= 4 and desvio <= 1.5) else 0
            
            # Salva os dados
            resultados.append({
                "trecho_id": ids_originais[i],
                "trecho_texto": trecho[:50] + "...", # Guarda só o começo para ref
                "topico_id": id_topico,
                "topico_nome": nome_topico,
                "scores_raw": str(scores),
                "n_validos": len(scores),
                "media_score": round(media, 2),
                "moda_score": moda,
                "desvio_padrao": round(desvio, 2),
                "classificado_positivo": classificacao_final,
                "confianca": "alta" if desvio <= 0.5 else "media" if desvio <= 1.0 else "baixa"
            })
        else:
            print(f"  -> Falha total para o tópico {nome_topico}")

# --- 5. EXPORTAÇÃO ---
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv(ARQUIVO_SAIDA, index=False)

print(f"\n--- Concluído em {round(time.time() - start_time, 2)} segundos ---")
print(f"Resultados salvos em: {ARQUIVO_SAIDA}")
print("\nExemplo dos primeiros resultados:")
print(df_resultados.head())