# Contexto Técnico - TesseraBot

## Stack Tecnológico Planejado

### Core Technologies
- **Python 3.9+**: Linguagem principal
- **Google Gemini**: LLM para geração de respostas (gratuito)
- **Discord.py**: Biblioteca para integração com Discord
- **LangChain**: Framework para RAG e processamento de documentos

### Processamento de Documentos
- **PyPDF2/pdfplumber**: Extração de texto de PDFs
- **sentence-transformers**: Embeddings para busca semântica
- **FAISS**: Banco vetorial local (gratuito)
- **spaCy**: Processamento de linguagem natural

### Armazenamento
- **SQLite**: Banco de dados local para metadados
- **Arquivos locais**: Armazenamento de embeddings e documentos

## Limitações Técnicas

### Hardware
- **RAM**: 8GB (necessário otimização de memória)
- **Storage**: ~100GB disponíveis
- **CPU**: Processamento local apenas

### Soluções para Limitações
- Processamento de documentos em lotes pequenos
- Uso de modelos de embedding leves
- Cache inteligente de respostas frequentes
- Compressão de índices vetoriais

## Dependências Principais
```
discord.py>=2.3.0
google-generativeai
langchain
langchain-community
sentence-transformers
faiss-cpu
pypdf2
sqlite3 (built-in)
python-dotenv
```

## Configuração de Desenvolvimento
- **Python virtual environment**: Isolamento de dependências
- **Git**: Controle de versão
- **VS Code**: IDE recomendada com extensões Python
- **Discord Developer Portal**: Configuração do bot

## Arquitetura de Alto Nível
1. **Document Ingestion**: Carrega e processa PDFs
2. **Vector Store**: Armazena embeddings localmente
3. **Query Processing**: Processa perguntas dos usuários
4. **Retrieval**: Busca documentos relevantes
5. **Generation**: Gera respostas com Gemini
6. **Discord Interface**: Apresenta respostas ao usuário

## Considerações de Performance
- Embeddings em lotes para otimizar RAM
- Cache de consultas frequentes
- Lazy loading de modelos
- Monitoramento de uso de memória