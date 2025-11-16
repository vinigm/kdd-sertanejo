import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminhos
base_dir = r"G:\Meu Drive\Mestrado\KDD\Anotacoes de aula\Trabalho pratico\projeto_funk"
arquivo_original = os.path.join(base_dir, "base_de_dados", "sertanejo_parcial_20251027_180724_pos600.csv")
arquivo_trechos = os.path.join(base_dir, "pre_processamento", "musicas_por_trechos_20251116_110519.csv")

print("="*70)
print("📊 ANÁLISE COMPLETA DOS DADOS COLETADOS")
print("="*70)
print()

# Carregar dados originais
df_original = pd.read_csv(arquivo_original)
print("📂 ARQUIVO ORIGINAL (base_de_dados)")
print("-"*70)
print(f"   Total de músicas coletadas: {len(df_original)}")
print(f"   Total de artistas diferentes: {df_original['artista'].nunique()}")
print(f"   Período: {int(df_original['ano'].min())} - {int(df_original['ano'].max())}")
print()

# Carregar dados processados
df_trechos = pd.read_csv(arquivo_trechos)
print("📂 ARQUIVO PROCESSADO (pre_processamento)")
print("-"*70)
print(f"   Total de trechos gerados: {len(df_trechos):,}")
print(f"   Média de trechos por música: {len(df_trechos)/df_trechos['tag_musica'].nunique():.1f}")
print()

# GRÁFICO 1: Estatísticas Gerais (Arquivo Original)
print("📊 Gerando Gráfico 1: Estatísticas Gerais...")
plt.figure(figsize=(10, 5))
dados = [len(df_original), df_original['artista'].nunique()]
labels = ['Músicas Coletadas', 'Artistas Únicos']
bars = plt.barh(labels, dados, color=['#2E86AB', '#A23B72'])

for i, v in enumerate(dados):
    plt.text(v + max(dados)*0.01, i, str(v), va='center', fontweight='bold', fontsize=12)

plt.title('Estatísticas da Coleta de Dados', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade', fontsize=11)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'grafico_1_estatisticas.png'), dpi=300, bbox_inches='tight')
print("   ✅ Salvo: grafico_1_estatisticas.png")

# GRÁFICO 2: Top 5 Artistas
print("📊 Gerando Gráfico 2: Top 5 Artistas...")
top_artistas = df_original['artista'].value_counts().head(5)

plt.figure(figsize=(10, 6))
bars = plt.barh(range(len(top_artistas)), top_artistas.values, color='#F18F01')
plt.yticks(range(len(top_artistas)), top_artistas.index)

for i, v in enumerate(top_artistas.values):
    plt.text(v + max(top_artistas.values)*0.01, i, str(v), va='center', fontweight='bold', fontsize=11)

plt.title('Top 5 Artistas com Mais Músicas Coletadas', fontsize=14, fontweight='bold')
plt.xlabel('Número de Músicas', fontsize=11)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'grafico_2_top_artistas.png'), dpi=300, bbox_inches='tight')
print("   ✅ Salvo: grafico_2_top_artistas.png")

# GRÁFICO 3: Distribuição por Ano
print("📊 Gerando Gráfico 3: Distribuição por Ano...")
anos_count = df_original['ano'].value_counts().sort_index()

plt.figure(figsize=(10, 7))
bars = plt.barh(range(len(anos_count)), anos_count.values, color='#C73E1D')
plt.yticks(range(len(anos_count)), [str(int(ano)) for ano in anos_count.index])

for i, v in enumerate(anos_count.values):
    plt.text(v + max(anos_count.values)*0.01, i, str(v), va='center', fontweight='bold', fontsize=10)

plt.title('Músicas Coletadas por Ano de Lançamento', fontsize=14, fontweight='bold')
plt.xlabel('Número de Músicas', fontsize=11)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'grafico_3_distribuicao_anos.png'), dpi=300, bbox_inches='tight')
print("   ✅ Salvo: grafico_3_distribuicao_anos.png")

# GRÁFICO 4: Comparação Base Original vs Processada
print("📊 Gerando Gráfico 4: Base Original vs Processada...")
plt.figure(figsize=(10, 5))
dados_comparacao = [len(df_original), len(df_trechos)]
labels_comparacao = ['Registros\n(Base Original)', 'Registros\n(Base Processada)']
colors = ['#2E86AB', '#06A77D']

bars = plt.barh(labels_comparacao, dados_comparacao, color=colors)

for i, v in enumerate(dados_comparacao):
    plt.text(v + max(dados_comparacao)*0.01, i, f'{v:,}', va='center', fontweight='bold', fontsize=12)

plt.title('Comparação: Base Original vs Base Processada', fontsize=14, fontweight='bold')
plt.xlabel('Número de Registros', fontsize=11)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'grafico_4_comparacao_bases.png'), dpi=300, bbox_inches='tight')
print("   ✅ Salvo: grafico_4_comparacao_bases.png")

# GRÁFICO 5: Trechos por Ano (da base processada)
print("📊 Gerando Gráfico 5: Trechos por Ano...")
trechos_por_ano = df_trechos[df_trechos['ano'].notna()].groupby('ano').size().sort_index()

plt.figure(figsize=(10, 7))
bars = plt.barh(range(len(trechos_por_ano)), trechos_por_ano.values, color='#9D4EDD')
plt.yticks(range(len(trechos_por_ano)), [str(int(ano)) for ano in trechos_por_ano.index])

for i, v in enumerate(trechos_por_ano.values):
    plt.text(v + max(trechos_por_ano.values)*0.01, i, str(v), va='center', fontweight='bold', fontsize=10)

plt.title('Trechos de Letras por Ano (Base Processada)', fontsize=14, fontweight='bold')
plt.xlabel('Número de Trechos', fontsize=11)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'grafico_5_trechos_por_ano.png'), dpi=300, bbox_inches='tight')
print("   ✅ Salvo: grafico_5_trechos_por_ano.png")

print()
print("="*70)
print("✅ TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
print("="*70)
print()
print("📊 RESUMO FINAL:")
print(f"   • {len(df_original)} músicas coletadas")
print(f"   • {df_original['artista'].nunique()} artistas diferentes")
print(f"   • {len(df_trechos):,} trechos gerados")
print(f"   • {len(anos_count)} anos diferentes representados")
print(f"   • {int(df_original['ano'].min())} - {int(df_original['ano'].max())}")
print()
print("📂 Arquivos gerados:")
print("   • grafico_1_estatisticas.png")
print("   • grafico_2_top_artistas.png")
print("   • grafico_3_distribuicao_anos.png")
print("   • grafico_4_comparacao_bases.png")
print("   • grafico_5_trechos_por_ano.png")
print("="*70)
