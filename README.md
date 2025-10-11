# Análise de Letras de Sertanejo e Funk

Este projeto contém ferramentas e análises para coleta e processamento de letras de música dos gêneros sertanejo e funk brasileiro.

## Estrutura do Projeto

### 📁 `funk_ai/`
Módulo focado na análise de letras de funk usando técnicas de inteligência artificial.

- **`codigo_sequencial.py`** - Código principal para processamento sequencial
- **`identificacao_topicos.ipynb`** - Notebook para identificação de tópicos nas letras
- **`scapper.ipynb`** - Notebook para configuração do ambiente Git
- **`README.md`** - Documentação específica do módulo funk

### 📁 `sertanejo_scraper/`
Módulo dedicado à coleta e análise de letras de música sertaneja.

#### Scripts de Coleta
- **`scraper_sertanejo.py`** - Scraper principal para letras sertanejas
- **`scraper_corrigido.py`** - Versão corrigida do scraper
- **`scraper_hits_lista.py`** - Coleta de hits populares
- **`scraper_mais_acessadas.py`** - Coleta das músicas mais acessadas
- **`scraper_ranking_otimizado.py`** - Scraper otimizado para rankings

#### Scripts de Configuração
- **`configurar_massivo.py`** - Configuração para coleta massiva
- **`configurar_estrategicos.py`** - Configuração de artistas estratégicos
- **`configurar_expansao.py`** - Configuração para expansão da base

#### Scripts de Análise
- **`analisar_dados.py`** - Análise geral dos dados coletados
- **`analisar_artistas.py`** - Análise específica de artistas
- **`analisar_base_moderna.py`** - Análise da base moderna (2023+)
- **`analisar_json.py`** - Análise de arquivos JSON
- **`relatorio_final.py`** - Geração de relatório final

#### Scripts de Processamento
- **`processar_anos_inteligente.py`** - Processamento inteligente por anos
- **`reprocessar_anos.py`** - Reprocessamento de dados por ano
- **`reprocessar_lote.py`** - Reprocessamento em lote

#### Scripts de Teste e Verificação
- **`teste_*.py`** - Diversos scripts de teste
- **`verificar_*.py`** - Scripts de verificação e validação
- **`debug_*.py`** - Scripts para depuração

#### Dados Gerados
- **`.csv`** - Arquivos de dados em formato CSV
- **`.json`** - Arquivos de dados em formato JSON
- **`.html`** - Páginas HTML para debug

### 📄 Arquivos de Documentação
- **`anotacoes.txt`** - Anotações do projeto
- **`excerpts_analysis.csv`** - Análise de trechos
- **`trabalhoPratico2025.pdf`** - Documento do trabalho prático

## Como Usar

### Pré-requisitos
- Python 3.7+
- Bibliotecas necessárias (ver requirements em cada módulo)

### Instalação
```bash
git clone https://github.com/vinigm/analise-letras-sertanejo.git
cd analise-letras-sertanejo
```

### Coleta de Dados Sertanejo
```bash
cd sertanejo_scraper
python scraper_sertanejo.py
```

### Análise de Funk
```bash
cd funk_ai
python codigo_sequencial.py
```

## Funcionalidades

- 🎵 **Coleta automatizada** de letras de música
- 📊 **Análise de tópicos** usando técnicas de NLP
- 🔍 **Processamento inteligente** por períodos temporais
- 📈 **Geração de relatórios** e visualizações
- 🎯 **Coleta estratégica** de artistas populares

## Dados Coletados

O projeto gera diversos tipos de dados:
- Letras de música com metadados
- Rankings de popularidade
- Análises temporais
- Identificação de tópicos
- Relatórios estatísticos

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autores

- Desenvolvido como parte do trabalho prático de Mestrado em KDD
- Análise de letras de música brasileira

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!