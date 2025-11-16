import pandas as pd

# Carregar os dois resultados
df_baseline = pd.read_csv('resultados_bertopic_baseline.csv')
df_stopwords = pd.read_csv('resultados_bertopic_com_stopwords.csv')

print("="*80)
print("COMPARAÇÃO: BASELINE (SEM STOPWORDS) vs COM STOPWORDS")
print("="*80)

print("\n### BASELINE (SEM STOPWORDS) ###")
print(f"Total de tópicos: {len(df_baseline)}")
print(f"Total de documentos: {df_baseline['Count'].sum()}")
print(f"Documentos no tópico -1 (outliers): {df_baseline[df_baseline['Topic'] == -1]['Count'].sum()}")
print("\nPrimeiros 15 tópicos:")
print(df_baseline[['Topic', 'Count', 'Name']].head(15).to_string())

print("\n" + "="*80)
print("\n### COM STOPWORDS ###")
print(f"Total de tópicos: {len(df_stopwords)}")
print(f"Total de documentos: {df_stopwords['Count'].sum()}")
print(f"Documentos no tópico -1 (outliers): {df_stopwords[df_stopwords['Topic'] == -1]['Count'].sum()}")
print("\nPrimeiros 15 tópicos:")
print(df_stopwords[['Topic', 'Count', 'Name']].head(15).to_string())

print("\n" + "="*80)
print("\n### DIFERENÇAS ###")
print(f"Mudança no número de tópicos: {len(df_stopwords) - len(df_baseline)}")
outliers_baseline = df_baseline[df_baseline['Topic'] == -1]['Count'].sum()
outliers_stopwords = df_stopwords[df_stopwords['Topic'] == -1]['Count'].sum()
print(f"Mudança nos outliers: {outliers_stopwords - outliers_baseline} ({outliers_stopwords/10722*100:.1f}% vs {outliers_baseline/10722*100:.1f}%)")

print("\n### PRINCIPAIS TÓPICOS - BASELINE ###")
for i, row in df_baseline[df_baseline['Topic'] != -1].head(5).iterrows():
    print(f"\nTópico {row['Topic']} ({row['Count']} docs): {row['Name']}")

print("\n### PRINCIPAIS TÓPICOS - COM STOPWORDS ###")
for i, row in df_stopwords[df_stopwords['Topic'] != -1].head(5).iterrows():
    print(f"\nTópico {row['Topic']} ({row['Count']} docs): {row['Name']}")
