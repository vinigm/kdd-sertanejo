import pandas as pd
import os
from datetime import datetime

def limpar_trechos_duplicados(arquivo_entrada, pasta_saida):
    """
    Remove trechos duplicados dentro de cada música.
    Mantém apenas a primeira ocorrência de cada trecho único.
    """
    
    print("="*70)
    print("🧹 LIMPEZA DE TRECHOS DUPLICADOS")
    print("="*70)
    print(f"📂 Arquivo de entrada: {os.path.basename(arquivo_entrada)}")
    print(f"📁 Pasta de saída: {pasta_saida}")
    print()
    
    # Carregar dados
    print("📖 Carregando dados...")
    df = pd.read_csv(arquivo_entrada)
    print(f"✅ Carregado: {len(df):,} trechos de {df['tag_musica'].nunique()} músicas")
    print()
    
    # Contar duplicatas antes da limpeza
    total_antes = len(df)
    
    # Remover trechos duplicados dentro de cada música
    print("🔄 Removendo trechos duplicados...")
    print("   Mantendo apenas a primeira ocorrência de cada trecho por música...")
    
    # Agrupar por música e remover duplicatas baseado no texto da letra
    # Usar drop_duplicates mantendo a primeira ocorrência
    df_limpo = df.drop_duplicates(subset=['tag_musica', 'letra'], keep='first')
    
    total_depois = len(df_limpo)
    removidos = total_antes - total_depois
    
    print(f"✅ Limpeza concluída!")
    print(f"   📊 Trechos antes: {total_antes:,}")
    print(f"   📊 Trechos depois: {total_depois:,}")
    print(f"   🗑️  Trechos removidos: {removidos:,} ({removidos/total_antes*100:.1f}%)")
    print()
    
    # Renumerar as tags dos trechos para ficarem sequenciais
    print("🔄 Renumerando tags dos trechos...")
    
    # Criar nova coluna com numeração sequencial por música
    df_limpo = df_limpo.sort_values(['tag_musica', 'tag_trecho']).reset_index(drop=True)
    
    # Renumerar dentro de cada música
    nova_tag_trecho = []
    for musica in df_limpo['tag_musica'].unique():
        indices = df_limpo[df_limpo['tag_musica'] == musica].index
        for i, idx in enumerate(indices, start=1):
            nova_tag_trecho.append(f"{musica}_trecho{i}")
    
    df_limpo['tag_trecho'] = nova_tag_trecho
    
    print(f"✅ Tags renumeradas sequencialmente!")
    print()
    
    # Estatísticas detalhadas
    print("📊 ESTATÍSTICAS POR MÚSICA")
    print("-"*70)
    
    # Calcular quantos trechos foram removidos por música
    trechos_antes = df.groupby('tag_musica').size()
    trechos_depois = df_limpo.groupby('tag_musica').size()
    
    # Músicas com mais duplicatas removidas
    duplicatas_por_musica = (trechos_antes - trechos_depois).sort_values(ascending=False)
    musicas_com_duplicatas = duplicatas_por_musica[duplicatas_por_musica > 0]
    
    if len(musicas_com_duplicatas) > 0:
        print(f"   Músicas com duplicatas: {len(musicas_com_duplicatas)}")
        print(f"   Músicas sem duplicatas: {df['tag_musica'].nunique() - len(musicas_com_duplicatas)}")
        print()
        print("   Top 10 músicas com mais duplicatas removidas:")
        for i, (tag_musica, qtd_removida) in enumerate(musicas_com_duplicatas.head(10).items(), 1):
            # Pegar o título da música
            titulo = df[df['tag_musica'] == tag_musica]['titulo'].iloc[0]
            artista = df[df['tag_musica'] == tag_musica]['artista'].iloc[0]
            antes = trechos_antes[tag_musica]
            depois = trechos_depois.get(tag_musica, 0)
            print(f"      {i:2d}. {titulo[:40]:40s} ({artista[:20]:20s})")
            print(f"          {int(antes)} → {int(depois)} trechos ({int(qtd_removida)} removidos)")
    else:
        print("   ✅ Nenhuma duplicata encontrada!")
    
    print()
    
    # Gerar nome do arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_saida = os.path.join(pasta_saida, f"musicas_por_trechos_limpo_{timestamp}.csv")
    
    # Salvar arquivo
    print(f"💾 Salvando arquivo limpo...")
    df_limpo.to_csv(arquivo_saida, index=False, encoding='utf-8')
    print(f"✅ Arquivo salvo: {os.path.basename(arquivo_saida)}")
    print()
    
    # Estatísticas finais
    print("="*70)
    print("📊 RESUMO FINAL")
    print("="*70)
    print(f"Total de trechos únicos: {len(df_limpo):,}")
    print(f"Total de músicas: {df_limpo['tag_musica'].nunique()}")
    print(f"Total de artistas: {df_limpo['artista'].nunique()}")
    print(f"Média de trechos por música: {len(df_limpo)/df_limpo['tag_musica'].nunique():.1f}")
    print()
    print(f"✅ Processamento finalizado com sucesso!")
    print(f"📂 Arquivo disponível em: {arquivo_saida}")
    print("="*70)
    
    return df_limpo, arquivo_saida


def main():
    """Função principal para executar a limpeza."""
    
    # Definir caminhos
    base_dir = r"G:\Meu Drive\Mestrado\KDD\Anotacoes de aula\Trabalho pratico\projeto_funk"
    pasta_pre_processamento = os.path.join(base_dir, "pre_processamento")
    
    # Encontrar o arquivo mais recente de trechos (não limpo)
    import glob
    arquivos_trechos = glob.glob(os.path.join(pasta_pre_processamento, "musicas_por_trechos_2*.csv"))
    
    # Filtrar apenas os arquivos que NÃO são limpos
    arquivos_trechos = [f for f in arquivos_trechos if 'limpo' not in f]
    
    if not arquivos_trechos:
        print("❌ Erro: Nenhum arquivo de trechos encontrado!")
        return
    
    # Pegar o arquivo mais recente
    arquivo_entrada = max(arquivos_trechos, key=os.path.getmtime)
    
    # Processar
    df_resultado, arquivo_saida = limpar_trechos_duplicados(arquivo_entrada, pasta_pre_processamento)
    
    # Mostrar exemplo de trechos após limpeza
    print("\n📝 EXEMPLO DOS PRIMEIROS TRECHOS (APÓS LIMPEZA):")
    print("="*70)
    print(df_resultado[['tag_musica', 'tag_trecho', 'titulo', 'artista', 'letra']].head(15).to_string(index=False))
    print("="*70)


if __name__ == "__main__":
    main()
