import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Arquivo específico - último arquivo gerado
arquivo_especifico = r"g:\Meu Drive\Mestrado\KDD\Anotacoes de aula\Trabalho pratico\projeto_funk\base_de_dados\sertanejo_mais_acessadas_todos_anos_1.csv"

# Carregar apenas o arquivo específico
df_complete = pd.read_csv(arquivo_especifico)
print(f"Carregado arquivo: {os.path.basename(arquivo_especifico)}")
print(f"Total de registros: {len(df_complete)}")

# GRÁFICO 1: Estatísticas Gerais
total_musicas = len(df_complete)
total_artistas = df_complete['artista'].nunique()

plt.figure(figsize=(10, 5))
dados = [total_musicas, total_artistas]
labels = ['Músicas Coletadas', 'Artistas Únicos']
bars = plt.barh(labels, dados, color=['blue', 'orange'])

for i, v in enumerate(dados):
    plt.text(v + max(dados)*0.01, i, str(v), va='center', fontweight='bold')

plt.title('Estatísticas da Coleta', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade')
plt.tight_layout()
plt.savefig('grafico_1_estatisticas.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO 2: Top 5 Artistas
top_artistas = df_complete['artista'].value_counts().head(5)

plt.figure(figsize=(10, 6))
bars = plt.barh(range(len(top_artistas)), top_artistas.values, color='green')
plt.yticks(range(len(top_artistas)), top_artistas.index)

for i, v in enumerate(top_artistas.values):
    plt.text(v + max(top_artistas.values)*0.01, i, str(v), va='center', fontweight='bold')

plt.title('Top 5 Artistas', fontsize=14, fontweight='bold')
plt.xlabel('Número de Músicas')
plt.tight_layout()
plt.savefig('grafico_2_artistas.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO 3: Distribuição por Ano
df_complete['ano'] = pd.to_numeric(df_complete['ano'], errors='coerce')
anos_count = df_complete['ano'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
bars = plt.barh(range(len(anos_count)), anos_count.values, color='red')
plt.yticks(range(len(anos_count)), [str(int(ano)) for ano in anos_count.index])

for i, v in enumerate(anos_count.values):
    plt.text(v + max(anos_count.values)*0.01, i, str(v), va='center', fontweight='bold')

plt.title('Músicas por Ano', fontsize=14, fontweight='bold')
plt.xlabel('Número de Músicas')
plt.tight_layout()
plt.savefig('grafico_3_anos.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Total: {total_musicas} músicas, {total_artistas} artistas")
print("Gráficos salvos: grafico_1_estatisticas.png, grafico_2_artistas.png, grafico_3_anos.png")