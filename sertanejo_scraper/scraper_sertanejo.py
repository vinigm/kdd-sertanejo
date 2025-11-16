# ================================================================================
# SCRAPER CORRIGIDO COM SELETORES ATUALIZADOS
# Baseado na análise da estrutura real das páginas
# ================================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import json
from datetime import datetime
from urllib.parse import urljoin, quote
import unidecode

def fazer_request(url):
    """Faz uma requisição HTTP e retorna o soup."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        return None

def extrair_ano_melhorado(soup):
    """Extrai o ano da música usando JSON-LD."""
    try:
        scripts_json = soup.find_all('script', type='application/ld+json')
        for script in scripts_json:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    for campo in ['datePublished', 'releaseDate', 'dateCreated', 'uploadDate']:
                        if campo in data:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(data[campo]))
                            if ano_match:
                                return int(ano_match.group())
                    
                    if data.get('@type') == 'MusicRecording' and 'inAlbum' in data:
                        album = data['inAlbum']
                        if isinstance(album, dict) and 'datePublished' in album:
                            ano_match = re.search(r'\b(19|20)\d{2}\b', str(album['datePublished']))
                            if ano_match:
                                return int(ano_match.group())
            except:
                continue
        return None
    except:
        return None

def limpar_letra(letra_bruta):
    """Limpa e formata o texto da letra."""
    if not letra_bruta:
        return ""
    
    # 1. Separar palavras grudadas - minúscula seguida de maiúscula
    texto_limpo = re.sub(r'([a-záéíóúçãõâêôà])([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ])', r'\1 \2', letra_bruta)
    
    # 2. Separar número seguido de letra maiúscula (ex: "IPVAQuem" -> "IPVA Quem")
    texto_limpo = re.sub(r'([0-9A-ZÁÉÍÓÚÇÃÕÂÊÔÀ]{2,})([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ][a-záéíóúçãõâêôà])', r'\1 \2', texto_limpo)
    
    # 3. Separar siglas grudadas em palavras (ex: "IPVAQuem" -> "IPVA Quem")
    texto_limpo = re.sub(r'([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ]{2,})([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ][a-záéíóúçãõâêôà]+)', r'\1 \2', texto_limpo)
    
    # 4. Separar palavra terminada seguida de palavra começada com maiúscula
    texto_limpo = re.sub(r'([a-záéíóúçãõâêôà])([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ][a-záéíóúçãõâêôà])', r'\1 \2', texto_limpo)
    
    # 5. Adicionar espaços após pontuação quando necessário
    texto_limpo = re.sub(r'([.!?;:])([A-ZÁÉÍÓÚÇÃÕÂÊÔÀ])', r'\1 \2', texto_limpo)
    
    # 6. Limpar espaços extras e quebras de linha
    linhas = [linha.strip() for linha in texto_limpo.split('\n') if linha.strip()]
    texto_final = '\n'.join(linhas)
    
    # 7. Remover espaços duplicados
    texto_final = re.sub(r'\s+', ' ', texto_final)
    
    return texto_final

def extrair_letra_completa_corrigida(url_musica, titulo_original, artista_original, ranking_pos):
    """Extrai letra completa usando seletores atualizados."""
    
    print(f"[{ranking_pos:3}] 🎵 {artista_original} - {titulo_original}")
    
    soup = fazer_request(url_musica)
    if not soup:
        print(f"      ❌ Erro ao acessar URL")
        return None
    
    try:
        # Novos seletores baseados na análise
        # Título: h1 dentro de textStyle-primary
        titulo_elem = soup.find('h1', class_='textStyle-primary')
        if not titulo_elem:
            # Fallback para outros seletores
            titulo_elem = soup.find('h1')
        
        if not titulo_elem:
            print(f"      ❌ Título não encontrado")
            return None
        
        titulo = titulo_elem.get_text(strip=True)
        
        # Artista: link para artista (geralmente próximo ao título)
        artista_elem = titulo_elem.find_next('a')
        if artista_elem and '/henrique-e-juliano/' in artista_elem.get('href', ''):
            artista = artista_elem.get_text(strip=True)
        else:
            # Fallback para artista original
            artista = artista_original
        
        # Letra: procurar diferentes classes
        seletores_letra = [
            '.lyric-original',
            '[class*="lyric"]',
            'div.lyric',
            '.letra'
        ]
        
        letra_elem = None
        for seletor in seletores_letra:
            letra_elem = soup.select_one(seletor)
            if letra_elem and len(letra_elem.get_text().strip()) > 100:
                break
        
        if not letra_elem:
            print(f"      ❌ Letra não encontrada")
            return None
        
        letra_bruta = letra_elem.get_text()
        letra_limpa = limpar_letra(letra_bruta)
        
        if len(letra_limpa.split()) < 10:
            print(f"      ⚠️ Letra muito curta")
            return None
        
        # Extrair ano
        ano = extrair_ano_melhorado(soup)
        
        # FILTRO REMOVIDO: Coletando músicas de todos os anos
        # if ano and ano < 2023:
        #     print(f"      ⏭️ Pulando música de {ano} (anterior a 2023)")
        #     return None
        
        # Se não tem ano, vamos incluir mesmo assim
        if not ano:
            print(f"      ⚠️ Ano não encontrado - incluindo mesmo assim")
        
        dados_musica = {
            'ranking_posicao': ranking_pos,
            'titulo': titulo,
            'artista': artista,
            'titulo_original': titulo_original,
            'artista_original': artista_original,
            'letra': letra_limpa,
            'url': url_musica,
            'ano': ano,
            'coletado_em': datetime.now().isoformat(),
            'contagem_palavras': len(letra_limpa.split()),
            'contagem_linhas': len(letra_limpa.split('\n')),
            'fonte': 'sertanejo_todos_anos'
        }
        
        ano_str = f", ano: {ano}" if ano else ", ano: não identificado"
        print(f"      ✅ Sucesso! ({dados_musica['contagem_palavras']} palavras{ano_str})")
        return dados_musica
        
    except Exception as e:
        print(f"      ❌ Erro: {str(e)}")
        return None

def normalizar_nome_url(texto):
    """Normaliza nome para URL do Letras.mus.br."""
    # Remover partes entre parênteses
    texto = re.sub(r'\s*\([^)]*\)\s*', '', texto)
    # Remover acentos
    texto = unidecode.unidecode(texto) if texto else ""
    # Converter para minúsculas
    texto = texto.lower()
    # Casos especiais
    texto = texto.replace('&', 'e')
    # Remover caracteres especiais
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    # Trocar espaços por hífens
    texto = re.sub(r'\s+', '-', texto)
    # Limpar hífens
    texto = re.sub(r'-+', '-', texto).strip('-')
    return texto

def construir_url_musica(titulo, artista):
    """Constrói URL da música."""
    artista_url = normalizar_nome_url(artista)
    titulo_url = normalizar_nome_url(titulo)
    return f"https://www.letras.mus.br/{artista_url}/{titulo_url}/"

def buscar_musicas_mais_acessadas(limite=1000):
    """Busca a lista real de músicas mais acessadas do sertanejo no site."""
    
    print(f"🔍 Buscando músicas mais acessadas do sertanejo (limite: {limite})...")
    print(f"⏱️  EXECUÇÃO LONGA: Preparado para coleta extensiva...")
    url_ranking = "https://www.letras.mus.br/mais-acessadas/sertanejo/"
    
    soup = fazer_request(url_ranking)
    if not soup:
        print(f"❌ Erro ao acessar página de ranking")
        return []
    
    musicas_encontradas = []
    urls_processadas = set()  # Evitar duplicatas
    
    try:
        # Procurar pela lista de músicas na página
        # Vamos tentar diferentes seletores baseados na estrutura comum do site
        
        # Seletor 1: Links que contêm títulos de músicas
        links_musicas = soup.find_all('a', href=True)
        
        contador = 0
        for link in links_musicas:
            if contador >= limite:
                break
                
            href = link.get('href', '')
            texto = link.get_text(strip=True)
            
            # Filtrar apenas links que parecem ser de músicas
            # Links de músicas geralmente têm o padrão: /artista/titulo/
            if (href.count('/') >= 3 and 
                not any(x in href.lower() for x in ['mais-acessadas', 'artista', 'album', 'biografia', 'playlists', 'estilos']) and
                href not in urls_processadas and
                href.startswith('/') and
                len(href.split('/')) >= 3):
                
                # Extrair artista e título do link ou texto
                if texto and len(texto) > 3:  # Evitar textos muito curtos
                    # Tentar extrair informações do próprio link
                    partes_url = href.strip('/').split('/')
                    if len(partes_url) >= 2:
                        artista_url = partes_url[-2]
                        titulo_url = partes_url[-1]
                        
                        # Filtrar URLs que não parecem ser de música
                        if any(x in titulo_url.lower() for x in ['biografia', 'discografia', 'fotos']):
                            continue
                        
                        # Converter de volta para texto legível
                        artista = artista_url.replace('-', ' ').title()
                        titulo = titulo_url.replace('-', ' ').title()
                        
                        # Evitar títulos muito curtos ou suspeitos
                        if len(titulo) < 2 or titulo.isdigit():
                            continue
                        
                        urls_processadas.add(href)
                        contador += 1
                        musicas_encontradas.append((contador, titulo, artista))
                        
                        if contador <= 15:  # Mostrar os primeiros 15
                            print(f"   {contador:2d}. {artista} - {titulo}")
        
        if contador > 15:
            print(f"   ... e mais {contador-15} músicas encontradas")
        
        # Para listas grandes, sempre tentar estratégia expandida
        if len(musicas_encontradas) < limite * 0.8:  # Se não conseguiu 80% do limite
            print(f"🔍 Expandindo busca... ({len(musicas_encontradas)} encontradas, buscando mais)")
            
            # Buscar em múltiplas páginas de sertanejo
            urls_adicionais = [
                "https://www.letras.mus.br/estilos/sertanejo/",
                "https://www.letras.mus.br/top100/sertanejo/",
                "https://www.letras.mus.br/estilos/sertanejo-universitario/",
                "https://www.letras.mus.br/estilos/sertanejo-raiz/",
            ]
            
            for url_adicional in urls_adicionais:
                if len(musicas_encontradas) >= limite:
                    break
                    
                print(f"🔍 Buscando em: {url_adicional}")
                soup_adicional = fazer_request(url_adicional)
                if soup_adicional:
                    links_adicionais = soup_adicional.find_all('a', href=True)
                    
                    for link in links_adicionais:
                        if len(musicas_encontradas) >= limite:
                            break
                            
                        href = link.get('href', '')
                        if (href.count('/') >= 3 and 
                            href not in urls_processadas and
                            not any(x in href.lower() for x in ['mais-acessadas', 'artista', 'album', 'biografia'])):
                            
                            partes_url = href.strip('/').split('/')
                            if len(partes_url) >= 2:
                                artista_url = partes_url[-2]
                                titulo_url = partes_url[-1]
                                
                                if not titulo_url.isdigit() and len(titulo_url) > 2:
                                    artista = artista_url.replace('-', ' ').title()
                                    titulo = titulo_url.replace('-', ' ').title()
                                    
                                    urls_processadas.add(href)
                                    musicas_encontradas.append((len(musicas_encontradas) + 1, titulo, artista))
            
        print(f"✅ Total encontrado: {len(musicas_encontradas)} músicas")
        
    except Exception as e:
        print(f"❌ Erro ao extrair lista: {str(e)}")
        return []
    
    return musicas_encontradas

def coletar_hits_automatico(limite=1000):
    """Coleta hits automaticamente da página mais acessadas."""
    
    print(f"🚀 COLETA AUTOMÁTICA MEGA - SERTANEJO MAIS ACESSADO")
    print("=" * 70)
    print(f"🎯 META AMBICIOSA: {limite} músicas")
    print(f"⏱️  Tempo estimado: {limite * 2.5 / 60:.0f} minutos (~{limite * 2.5 / 3600:.1f} horas)")
    print(f"💤 EXECUÇÃO LONGA: Pode deixar rodando...")
    
    # Buscar lista real do site
    musicas_lista = buscar_musicas_mais_acessadas(limite)
    
    if not musicas_lista:
        print("❌ Não foi possível obter a lista de músicas. Usando lista manual de backup...")
        return coletar_hits_corrigido()
    
    print(f"✅ Lista encontrada: {len(musicas_lista)} músicas para processar")
    
    if len(musicas_lista) < 500:
        print(f"⚠️  Lista tem {len(musicas_lista)} músicas (menos que 500). Continuando mesmo assim...")
    elif len(musicas_lista) >= 800:
        print(f"🎉 EXCELENTE! Lista com {len(musicas_lista)} músicas encontradas!")
    
    return coletar_letras_da_lista(musicas_lista)

def coletar_hits_corrigido():
    """Coleta hits usando lista manual (backup)."""
    
    print(f"🚀 COLETA DE HITS - VERSÃO MANUAL")
    print("=" * 70)
    
    # Lista de teste para verificar coleta sem filtro de ano
    musicas_teste = [
        # Músicas de diferentes épocas para testar a coleta ampla
        (1, "Amor Dos Outros", "Henrique & Juliano"),
        (2, "Seja Ex", "Henrique & Juliano"),
        (3, "OLHO MARROM", "Luan Santana"),
        (4, "Retrovisor", "Gusttavo Lima"),
        (5, "Telefone Mudo", "Henrique & Juliano"),
        
        # Músicas mais antigas (para testar o filtro)
        (6, "Evidências", "Chitãozinho & Xororó"),  # Antiga
        (7, "Infiel", "Marília Mendonça"),          # 2015
        (8, "Balada", "Gusttavo Lima"),             # 2011
        (9, "Boate Azul", "Bruno & Marrone"),       # Antiga
        (10, "Tocando Em Frente", "Almir Sater"),   # 1991
    ]
    
    return coletar_letras_da_lista(musicas_teste)

def salvar_dados_parciais(musicas_coletadas, posicao_atual):
    """Salva dados parciais para evitar perda em execuções longas."""
    if musicas_coletadas:
        import os
        df = pd.DataFrame(musicas_coletadas)
        
        # Criar nome do arquivo parcial
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo_parcial = f"../base_de_dados/sertanejo_parcial_{timestamp}_pos{posicao_atual}.csv"
        
        df.to_csv(arquivo_parcial, index=False, encoding='utf-8')
        print(f"     📁 Backup salvo: {os.path.basename(arquivo_parcial)}")

def coletar_letras_da_lista(musicas_lista):
    """Coleta letras de uma lista de músicas de todos os anos."""
    
    print(f"🎵 Coletando {len(musicas_lista)} músicas sertanejas populares...")
    print(f"📅 SEM FILTRO: Coletando músicas de todos os anos!")
    print(f"💾 Dados serão salvos em: ../base_de_dados/")
    print(f"⏱️  Tempo estimado: {(len(musicas_lista) * 3 / 60):.1f} minutos")
    
    musicas_coletadas = []
    sucessos = 0
    falhas = 0
    filtradas = 0
    
    # Progresso visual otimizado para listas grandes
    if len(musicas_lista) > 500:
        checkpoint = 50  # A cada 50 músicas para listas muito grandes
    elif len(musicas_lista) > 200:
        checkpoint = 25  # A cada 25 músicas para listas grandes
    else:
        checkpoint = 10  # A cada 10 músicas para listas pequenas
    
    inicio_tempo = time.time()
    
    for i, (posicao, titulo, artista) in enumerate(musicas_lista, 1):
        # Mostrar progresso detalhado
        if i % checkpoint == 0 or i == len(musicas_lista):
            progresso = (i / len(musicas_lista)) * 100
            tempo_decorrido = time.time() - inicio_tempo
            tempo_por_musica = tempo_decorrido / i
            tempo_restante = (len(musicas_lista) - i) * tempo_por_musica
            
            print(f"\n📊 PROGRESSO: {progresso:.1f}% ({i}/{len(musicas_lista)})")
            print(f"   ✅ Sucessos: {sucessos} | ❌ Falhas: {falhas} | 📈 Taxa: {sucessos/i*100:.1f}%")
            print(f"   ⏱️  Tempo decorrido: {tempo_decorrido/60:.1f}min | Restante: ~{tempo_restante/60:.0f}min")
            
            # Salvar progresso parcial a cada checkpoint
            if sucessos > 0 and i % (checkpoint * 2) == 0:
                print(f"   💾 Salvando progresso parcial...")
                salvar_dados_parciais(musicas_coletadas, i)
        
        url = construir_url_musica(titulo, artista)
        
        try:
            dados = extrair_letra_completa_corrigida(url, titulo, artista, posicao)
            
            if dados:
                musicas_coletadas.append(dados)
                sucessos += 1
            else:
                falhas += 1
        except Exception as e:
            print(f"      ❌ Erro inesperado: {str(e)}")
            falhas += 1
        
        # Delay otimizado para execuções longas
        if len(musicas_lista) > 500:
            time.sleep(random.uniform(1.0, 2.0))  # Delay mais rápido para listas muito grandes
        elif len(musicas_lista) > 100:
            time.sleep(random.uniform(1.5, 2.5))  # Delay moderado para listas grandes
        else:
            time.sleep(random.uniform(2, 4))  # Delay normal para listas pequenas
    
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADO FINAL:")
    print(f"   ✅ Sucessos: {sucessos}")
    print(f"   ❌ Falhas: {falhas}")
    print(f"   📈 Taxa de sucesso: {(sucessos/(sucessos+falhas)*100):.1f}%")
    
    if len(musicas_lista) >= 200:
        if sucessos >= 200:
            print(f"   🎯 EXCELENTE! Meta de 200+ músicas ATINGIDA!")
        elif sucessos >= 150:
            print(f"   ✅ MUITO BOM! Próximo da meta (150+)")
        elif sucessos >= 100:
            print(f"   ⚠️  BOM resultado, mas abaixo da meta")
        else:
            print(f"   ⚠️  Resultado abaixo do esperado para lista grande")
    
    if musicas_coletadas:
        # Salvar dados na pasta base_de_dados com numeração sequencial
        df = pd.DataFrame(musicas_coletadas)
        
        # Encontrar o próximo número disponível
        import os
        base_nome = "sertanejo_mais_acessadas_todos_anos"
        contador = 1
        while os.path.exists(f"../base_de_dados/{base_nome}_{contador}.csv"):
            contador += 1
        
        arquivo = f"../base_de_dados/{base_nome}_{contador}.csv"
        df.to_csv(arquivo, index=False, encoding='utf-8')
        
        print(f"💾 Dados salvos em: {arquivo}")
        
        # Análises detalhadas
        total_palavras = df['contagem_palavras'].sum()
        musicas_com_ano = df[df['ano'].notna()]
        
        print(f"\n📊 ANÁLISE DETALHADA:")
        print(f"   📝 Total de palavras: {total_palavras:,}")
        print(f"   📊 Média por música: {df['contagem_palavras'].mean():.0f} palavras")
        print(f"   📅 Músicas com ano: {len(musicas_com_ano)}")
        print(f"   📈 Músicas sem ano: {len(df) - len(musicas_com_ano)} (incluídas como possivelmente modernas)")
        
        if len(musicas_com_ano) > 0:
            anos = musicas_com_ano['ano'].value_counts().sort_index()
            print(f"   🗓️  Anos encontrados: {list(anos.index)}")
            
            # Estatísticas por ano
            for ano in sorted(anos.index):
                qtd = anos[ano]
                print(f"      - {ano}: {qtd} músicas")
    
    return musicas_coletadas

if __name__ == "__main__":
    print("🚀 SCRAPER MEGA - SERTANEJO DE TODOS OS ANOS")
    print("🎯 META AMBICIOSA: Coletar até 1000 músicas")
    print("⏱️  EXECUÇÃO LONGA: Pode levar algumas horas")
    print("💾 BACKUP AUTOMÁTICO: Salvamento periódico habilitado")
    print("🔄 ROBUSTO: Resistente a falhas e interrupções")
    print()
    
    inicio_execucao = time.time()
    
    # Usar a nova função automática com limite máximo
    musicas = coletar_hits_automatico(limite=1000)
    
    tempo_total = time.time() - inicio_execucao
    
    print(f"\n" + "="*70)
    print(f"🏁 EXECUÇÃO FINALIZADA!")
    print(f"⏱️  Tempo total: {tempo_total/60:.1f} minutos ({tempo_total/3600:.1f} horas)")
    print(f"📊 Total coletado: {len(musicas)} músicas")
    
    # Avaliação dos resultados
    if len(musicas) >= 800:
        print(f"   � EXCEPCIONAL! Mais de 800 músicas coletadas!")
        print(f"   🎯 Dataset mega robusto para análises!")
    elif len(musicas) >= 500:
        print(f"   🎉 EXCELENTE! Mais de 500 músicas coletadas!")
        print(f"   ✅ Dataset muito bom para análises profundas!")
    elif len(musicas) >= 300:
        print(f"   ✅ MUITO BOM! Mais de 300 músicas coletadas!")
        print(f"   📊 Dataset sólido para análises!")
    elif len(musicas) >= 200:
        print(f"   ✅ BOM! Mais de 200 músicas coletadas!")
    elif len(musicas) >= 100:
        print(f"   ⚠️ Moderado. Mais de 100 músicas obtidas.")
    else:
        print(f"   ⚠️ Resultado abaixo do esperado.")
    
    if len(musicas) > 0:
        taxa_por_minuto = len(musicas) / (tempo_total / 60)
        print(f"📈 Velocidade média: {taxa_por_minuto:.1f} músicas/minuto")