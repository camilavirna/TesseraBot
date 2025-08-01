# 🎓 TesseraBot - Assistente Universitário com IA

Bot Discord inteligente que ajuda universitários com dúvidas sobre matrícula, cronogramas e procedimentos acadêmicos usando RAG (Retrieval-Augmented Generation) com documentos PDF da universidade.

## ✨ Características

- 🤖 **Arquitetura Modular**: Core Engine independente de plataforma
- 💬 **Conversação Natural**: Respostas contextualizadas para ambiente universitário  
- 📚 **RAG com PDFs**: Busca informações em documentos oficiais (em desenvolvimento)
- 🔄 **Multi-plataforma**: Preparado para Discord, Telegram, Web
- 🛡️ **Seguro**: Configuração via variáveis de ambiente
- 💾 **Local**: Processamento local, sem dependência de nuvem

## 🚀 Funcionalidades

### ✅ Implementado
- Bot Discord funcional
- Integração com Google Gemini 1.5 Flash
- Comandos: `!help`, `!status`, `!test`
- Conversa natural: `tesserabot [sua pergunta]`
- Arquitetura preparada para RAG

### 🔄 Em Desenvolvimento
- Processamento de PDFs universitários
- Sistema RAG com FAISS local
- Busca semântica em documentos
- Cache inteligente de respostas

## 📋 Pré-requisitos

- Python 3.9+
- Conta Discord Developer
- API Key Google Gemini (gratuita)
- ~6GB RAM disponível
- ~100GB storage

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/[seu-usuario]/tesserabot.git
cd tesserabot
```

### 2. Crie ambiente virtual
```bash
python -m venv tesserabot_env
tesserabot_env\Scripts\activate  # Windows
# ou
source tesserabot_env/bin/activate  # Linux/Mac
```

### 3. Instale dependências
```bash
pip install discord.py==2.3.2 google-generativeai==0.3.2 python-dotenv==1.0.0
```

### 4. Configure variáveis de ambiente
Crie arquivo `.env` na raiz:
```env
DISCORD_BOT_TOKEN=seu_token_discord_aqui
GOOGLE_API_KEY=sua_chave_gemini_aqui
BOT_PREFIX=!
BOT_NAME=TesseraBot
```

### 5. Execute o bot
```bash
python src/main.py
```

## 📖 Como usar

### Comandos
- `!help` - Mostra ajuda
- `!status` - Status do bot
- `!test [pergunta]` - Testa o Core Engine

### Conversa Natural
```
tesserabot qual a data da matrícula?
tesserabot que documentos preciso para me matricular?
```

## 🏗️ Arquitetura

```
📁 TesseraBot/
├── 🧠 src/core/bot_engine.py           # Core Engine (independente)
├── 🤖 src/adapters/discord_adapter.py  # Interface Discord
├── 🚀 src/main.py                      # Ponto de entrada
├── 📂 data/                            # Documentos e dados
├── ⚙️ config/                          # Configurações
└── 📚 memory-bank/                     # Documentação técnica
```

### Core Engine
- **Independente de plataforma**: Reutilizável para Discord, Telegram, Web
- **Processamento de IA**: Integração com Google Gemini
- **RAG preparado**: Estrutura para busca em documentos

### Discord Adapter
- **Event-driven**: Responde a mensagens e comandos
- **Formatação rica**: Embeds e respostas estruturadas
- **Debug integrado**: Logs detalhados para desenvolvimento

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 🔗 Links Úteis

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Documentação Gemini](https://ai.google.dev/docs)

## 📞 Suporte

Se você tiver problemas:
1. Verifique os logs no terminal
2. Confirme as chaves API no arquivo `.env`
3. Abra uma issue descrevendo o problema

---

**Feito com ❤️ para ajudar universitários**