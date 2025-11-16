import pandas as pd
import os
from datetime import datetime

def processar_letras_em_trechos(arquivo_entrada, pasta_saida):
    """
    Processa o arquivo de músicas e cria uma nova tabela com os trechos das letras.
    Cada linha da letra vira uma linha na nova tabela.
    """
    
    print("="*70)
    print("🎵 PROCESSAMENTO DE TRECHOS DE LETRAS")
    print("="*70)
    print(f"📂 Arquivo de entrada: {os.path.basename(arquivo_entrada)}")
    print(f"📁 Pasta de saída: {pasta_saida}")
    print()
    
    # Carregar dados originais
    print("📖 Carregando dados originais...")
    df_original = pd.read_csv(arquivo_entrada)
    print(f"✅ Carregado: {len(df_original)} músicas")
    print()
    
    # Lista para armazenar os novos dados
    dados_processados = []
    
    # Processar cada música
    print("🔄 Processando músicas e quebrando letras em trechos...")
    total_trechos = 0
    
    for idx, row in df_original.iterrows():
        num_musica = idx + 1  # Número da música (começa em 1)
        tag_musica = f"musica{num_musica}"  # Tag no formato musica1, musica2, etc
        
        # Pegar a letra completa
        letra_completa = str(row['letra']) if pd.notna(row['letra']) else ""
        
        # Quebrar a letra em versos usando estratégias inteligentes
        # 1. Tentar quebrar por \n (quebras de linha explícitas)
        if '\n' in letra_completa:
            versos = [verso.strip() for verso in letra_completa.split('\n') if verso.strip()]
        else:
            # 2. Se não tem \n, quebrar quando encontrar letra maiúscula após espaço
            # Isso indica o início de um novo verso
            import re
            
            # Usar regex para quebrar antes de cada letra maiúscula que vem após um espaço
            # Padrão: espaço seguido de letra maiúscula
            # Mantém a maiúscula no início do novo verso
            versos_raw = re.split(r'(?<=\s)(?=[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ])', letra_completa)
            
            # Limpar espaços e filtrar versos vazios
            versos = [verso.strip() for verso in versos_raw if verso.strip()]
        
        # Se mesmo assim não conseguiu quebrar, usar toda a letra como um verso
        if not versos:
            versos = [letra_completa]
        
        # Criar uma linha para cada verso
        for num_verso, verso in enumerate(versos, start=1):
            tag_trecho = f"{tag_musica}_trecho{num_verso}"
            
            # Contar palavras do trecho
            contagem_palavras_trecho = len(verso.split())
            
            # Criar registro do trecho
            trecho_data = {
                'ranking_posicao': row['ranking_posicao'] if pd.notna(row['ranking_posicao']) else None,
                'titulo': row['titulo'],
                'tag_musica': tag_musica,
                'tag_trecho': tag_trecho,
                'letra': verso,  # O trecho/verso
                'artista': row['artista'],
                'ano': row['ano'] if pd.notna(row['ano']) else None,
                'contagem_palavras': contagem_palavras_trecho
            }
            
            dados_processados.append(trecho_data)
            total_trechos += 1
        
        # Mostrar progresso a cada 50 músicas
        if (idx + 1) % 50 == 0:
            print(f"   Processadas {idx + 1}/{len(df_original)} músicas - {total_trechos} trechos gerados")
    
    print(f"✅ Processamento concluído!")
    print(f"   📊 Total de músicas processadas: {len(df_original)}")
    print(f"   📝 Total de trechos gerados: {total_trechos}")
    print(f"   📈 Média de trechos por música: {total_trechos/len(df_original):.1f}")
    print()
    
    # Criar DataFrame com os trechos
    df_trechos = pd.DataFrame(dados_processados)
    
    # Gerar nome do arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_saida = os.path.join(pasta_saida, f"musicas_por_trechos_{timestamp}.csv")
    
    # Salvar arquivo
    print(f"💾 Salvando arquivo processado...")
    df_trechos.to_csv(arquivo_saida, index=False, encoding='utf-8')
    print(f"✅ Arquivo salvo: {os.path.basename(arquivo_saida)}")
    print()
    
    # Estatísticas
    print("="*70)
    print("📊 ESTATÍSTICAS DO ARQUIVO GERADO")
    print("="*70)
    print(f"Total de linhas (trechos): {len(df_trechos):,}")
    print(f"Total de músicas únicas: {df_trechos['tag_musica'].nunique()}")
    print(f"Total de artistas únicos: {df_trechos['artista'].nunique()}")
    
    # Distribuição de trechos
    trechos_por_musica = df_trechos.groupby('tag_musica').size()
    print(f"\nDistribuição de trechos por música:")
    print(f"   Mínimo: {trechos_por_musica.min()} trechos")
    print(f"   Máximo: {trechos_por_musica.max()} trechos")
    print(f"   Média: {trechos_por_musica.mean():.1f} trechos")
    print(f"   Mediana: {trechos_por_musica.median():.0f} trechos")
    
    # Verificar anos
    anos_validos = df_trechos[df_trechos['ano'].notna()]
    if len(anos_validos) > 0:
        print(f"\nDistribuição por ano:")
        anos_count = df_trechos[df_trechos['ano'].notna()]['ano'].value_counts().sort_index()
        for ano, count in anos_count.items():
            print(f"   {int(ano)}: {count} trechos")
    
    print()
    print(f"✅ Processamento finalizado com sucesso!")
    print(f"📂 Arquivo disponível em: {arquivo_saida}")
    print("="*70)
    
    return df_trechos, arquivo_saida


def main():
    """Função principal para executar o processamento."""
    
    # Definir caminhos
    base_dir = r"G:\Meu Drive\Mestrado\KDD\Anotacoes de aula\Trabalho pratico\projeto_funk"
    arquivo_entrada = os.path.join(base_dir, "base_de_dados", "sertanejo_parcial_20251027_180724_pos600.csv")
    pasta_saida = os.path.join(base_dir, "pre_processamento")
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Erro: Arquivo não encontrado: {arquivo_entrada}")
        return
    
    # Verificar se a pasta de saída existe
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"📁 Pasta criada: {pasta_saida}")
    
    # Processar
    df_resultado, arquivo_saida = processar_letras_em_trechos(arquivo_entrada, pasta_saida)
    
    # Mostrar exemplo dos primeiros trechos
    print("\n📝 EXEMPLO DOS PRIMEIROS TRECHOS:")
    print("="*70)
    print(df_resultado[['tag_musica', 'tag_trecho', 'titulo', 'artista', 'letra']].head(10).to_string(index=False))
    print("="*70)


if __name__ == "__main__":
    main()
