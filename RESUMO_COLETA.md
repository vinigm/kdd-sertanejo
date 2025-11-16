# 📊 RESUMO DA COLETA E PROCESSAMENTO - ANÁLISE LETRAS SERTANEJO

## 🎵 DADOS COLETADOS

### Base Original (base_de_dados/)
- **Total de músicas:** 557
- **Total de artistas:** 111 artistas diferentes
- **Período coberto:** 1982 - 2025 (43 anos)
- **Arquivo:** `sertanejo_parcial_20251027_180724_pos600.csv`

### Base Processada (pre_processamento/)
- **Total de trechos:** 16.521 trechos
- **Média de trechos por música:** ~29.7 trechos
- **Arquivo:** `musicas_por_trechos_20251116_110519.csv`

---

## 📈 TOP 5 ARTISTAS COM MAIS MÚSICAS

1. **Henrique & Juliano** - Maior número de músicas na base
2. **Gusttavo Lima** - Segundo maior
3. **Jorge & Mateus** - Terceiro maior
4. **Luan Santana** - Quarto maior
5. **Marilia Mendonca** - Quinto maior

---

## 📅 DISTRIBUIÇÃO POR DÉCADA

### Anos 1980-1990 (Sertanejo Raiz)
- **1982:** 1 música
- **1987:** 1 música
- **1990:** 1 música
- **1996:** 1 música
- **Total:** 4 músicas

### Anos 2010-2019 (Sertanejo Universitário)
- **2011-2015:** 118 músicas
- **2016-2019:** 117 músicas
- **Total:** 235 músicas

### Anos 2020-2025 (Sertanejo Moderno)
- **2020-2022:** 64 músicas
- **2023-2025:** 254 músicas
- **Total:** 318 músicas

---

## 🔄 PROCESSAMENTO REALIZADO

### O que foi feito:
1. **Coleta de dados:** Scraping de letras do site Letras.mus.br
2. **Remoção do filtro de ano:** Coletadas músicas de todas as épocas (não apenas 2023+)
3. **Quebra em trechos:** Cada letra foi dividida em trechos de 8-12 palavras

### Estrutura da Base Processada:
- `ranking_posicao`: Posição no ranking
- `titulo`: Nome da música
- `tag_musica`: ID único da música (1 a 557)
- `tag_trecho`: ID do trecho (ex: trecho1_1, trecho1_2, etc)
- `letra`: Conteúdo do trecho
- `artista`: Nome do artista
- `ano`: Ano de lançamento
- `contagem_palavras`: Número de palavras no trecho

---

## 📊 GRÁFICOS GERADOS

1. **grafico_1_estatisticas.png** - Estatísticas gerais (músicas e artistas)
2. **grafico_2_top_artistas.png** - Top 5 artistas com mais músicas
3. **grafico_3_distribuicao_anos.png** - Distribuição de músicas por ano
4. **grafico_4_comparacao_bases.png** - Comparação base original vs processada
5. **grafico_5_trechos_por_ano.png** - Distribuição de trechos por ano

---

## 💡 INSIGHTS

### Crescimento Temporal
- **Boom do sertanejo universitário:** Pico em 2014-2015
- **Nova onda:** Forte crescimento de 2023-2025 (254 músicas)
- **Representatividade histórica:** Presença de clássicos dos anos 80-90

### Diversidade
- 111 artistas diferentes demonstram boa diversidade
- Média de 5 músicas por artista
- Cobertura de 43 anos de história do gênero

### Base Processada
- Expansão de 557 para 16.521 registros
- Permite análises mais granulares a nível de trechos
- Facilita análises de linguagem e padrões textuais

---

## 📁 ESTRUTURA DE ARQUIVOS

```
projeto_funk/
├── base_de_dados/
│   └── sertanejo_parcial_20251027_180724_pos600.csv (557 músicas)
├── pre_processamento/
│   ├── processar_trechos.py (script de processamento)
│   └── musicas_por_trechos_20251116_110519.csv (16.521 trechos)
├── sertanejo_scraper/
│   └── scraper_sertanejo.py (script de coleta)
├── grafico_1_estatisticas.png
├── grafico_2_top_artistas.png
├── grafico_3_distribuicao_anos.png
├── grafico_4_comparacao_bases.png
├── grafico_5_trechos_por_ano.png
└── graficos_apresentacao_atualizado.py
```

---

## ✅ PRÓXIMOS PASSOS SUGERIDOS

1. **Análise de Sentimentos:** Identificar emoções predominantes por época
2. **Análise de Tópicos:** Descobrir temas recorrentes nas letras
3. **Análise de Vocabulário:** Comparar riqueza lexical entre décadas
4. **Análise de Coocorrência:** Palavras que aparecem juntas
5. **Modelagem:** Word2Vec, TF-IDF, etc.

---

**Data do Processamento:** 16/11/2025
**Repositório:** https://github.com/vinigm/kdd-sertanejo
