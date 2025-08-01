# Contexto Ativo - TesseraBot

## Estado Atual
**Status**: Bot Discord funcionando - Core Engine operacional
**Data**: Janeiro 2025
**Foco Principal**: Sistema RAG com PDFs universitários (próxima fase)

## Trabalho Atual
### Completado ✓
- **Memory Bank completa** criada e atualizada
- **Arquitetura modular** implementada (Core Engine + Discord Adapter)
- **Environment setup** (Python virtual env + dependências limpas)
- **Core Engine** com Gemini 1.5 Flash funcionando
- **Discord Bot** conectado e responsivo
- **Comandos básicos**: !help, !status, !test, !debug
- **Conversa natural**: "tesserabot [pergunta]" funcional
- **Repositório GitHub** preparado (.gitignore + README)

### Em Progresso 🔄
- **Documentação**: Atualizando Memory Bank para refletir progresso atual
- **Pausa temporária**: Usuário retornará para continuar de onde parou

### Próximos Passos 📋
1. **Sistema RAG (Fase 2)**
   - Instalar dependências RAG (langchain, sentence-transformers, faiss-cpu)
   - Implementar processador de PDF universitário
   - Criar sistema de embeddings e busca semântica
   - Integrar busca com geração de respostas

2. **Polimento**
   - Corrigir menções Discord (@TesseraBot)
   - Remover logs de debug excessivos
   - Adicionar cache de respostas

3. **Testes com Dados Reais**
   - Carregar PDFs da universidade
   - Ajustar prompts para contexto específico
   - Validar qualidade das respostas

## Decisões Ativas
### Arquitetura
- **Confirmado**: Usar FAISS local para vector store
- **Confirmado**: SQLite para metadados
- **Confirmado**: LangChain como framework principal
- **Pendente**: Estratégia específica de chunking para PDFs

### Desenvolvimento
- **Confirmado**: Desenvolvimento incremental com testes frequentes
- **Confirmado**: Código documentado para aprendizado do usuário
- **Pendente**: Estrutura de testes unitários

## Riscos e Mitigações
### Alto Risco
- **RAM limitada**: Processar documentos em lotes pequenos
- **Storage limitado**: Compressão de embeddings, limpeza regular

### Médio Risco
- **Qualidade dos PDFs**: Implementar fallbacks para OCR se necessário
- **Latência do Gemini**: Cache local para consultas frequentes

## Aprendizado do Usuário
O usuário tem nível iniciante em Python e quer aprender durante o desenvolvimento:
- Explicar conceitos conforme implementamos
- Código bem comentado
- Estrutura modular para entendimento gradual
- Exemplos práticos de cada componente

## Recursos Necessários
- Chave API do Google Gemini (gratuita)
- Token do bot Discord
- ~100 PDFs da universidade
- Python 3.9+ instalado