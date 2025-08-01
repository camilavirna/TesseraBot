"""
Core Bot Engine - O Cérebro Independente de Plataforma

Este é o núcleo do TesseraBot. Ele processa perguntas e gera respostas
independente de onde a pergunta veio (Discord, Telegram, Web, etc.).

Conceitos que você vai aprender aqui:
- Separation of Concerns (separação de responsabilidades)
- Dependency Injection (injeção de dependência)
- Abstract Base Classes (classes abstratas)
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

@dataclass
class BotResponse:
    """
    Representa uma resposta do bot.
    
    Por que usar dataclass?
    - Reduz código boilerplate
    - Fornece métodos úteis automaticamente (__init__, __repr__, etc.)
    - Deixa o código mais limpo e legível
    """
    content: str
    confidence: float = 0.0
    sources: list = None
    timestamp: datetime = None
    error: Optional[str] = None
    
    def __post_init__(self):
        """Executa após __init__ para definir valores padrão"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.sources is None:
            self.sources = []

class TesseraBotEngine:
    """
    O motor principal do TesseraBot.
    
    Esta classe é completamente independente de Discord, Telegram ou qualquer
    plataforma específica. Ela apenas:
    1. Recebe uma pergunta (string)
    2. Processa usando IA
    3. Retorna uma resposta estruturada
    
    Por que fazer assim?
    - Reutilização: mesmo código funciona no Discord, Telegram, Web
    - Testabilidade: fácil de testar sem dependências externas
    - Manutenção: mudanças no core não afetam as interfaces
    """
    
    def __init__(self):
        """
        Inicializa o motor do bot.
        
        Conceito: Lazy Loading
        - Só carrega o que precisa, quando precisa
        - Economiza memória (importante no nosso caso!)
        """
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.bot_name = os.getenv('BOT_NAME', 'TesseraBot')
        self.is_initialized = False
        self._setup_gemini()
        
    def _setup_gemini(self):
        """
        Configura a API do Google Gemini.
        
        Por que método privado (_setup_gemini)?
        - Não queremos que código externo chame isso diretamente
        - É uma responsabilidade interna da classe
        """
        try:
            if not self.google_api_key:
                raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
            
            genai.configure(api_key=self.google_api_key)
            
            # Configura o modelo Gemini com parâmetros otimizados
            model_name = "gemini-1.5-flash"
            print(f"🤖 Configurando modelo Gemini: {model_name}")
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={
                    "temperature": 0.3,  # Baixo = mais consistente, alto = mais criativo
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,  # Controla tamanho da resposta
                }
            )
            
            self.is_initialized = True
            print(f"✅ {self.bot_name} engine inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar Gemini: {e}")
            self.is_initialized = False
    
    async def process_message(self, user_message: str, user_context: Dict[str, Any] = None) -> BotResponse:
        """
        Processa uma mensagem do usuário e retorna uma resposta.
        
        Args:
            user_message: A pergunta/mensagem do usuário
            user_context: Contexto adicional (nome do usuário, histórico, etc.)
            
        Returns:
            BotResponse: Resposta estruturada com conteúdo e metadados
            
        Por que async?
        - Chamadas para APIs são lentas (rede)
        - async permite que outras operações continuem enquanto espera
        - Essencial para bots que atendem múltiplos usuários
        """
        
        if not self.is_initialized:
            return BotResponse(
                content="❌ Bot não está configurado corretamente. Verifique as chaves da API.",
                error="Gemini não inicializado"
            )
        
        try:
            # Contexto padrão para perguntas universitárias
            if user_context is None:
                user_context = {}
            
            # Monta o prompt com contexto universitário
            system_prompt = self._build_university_prompt(user_message, user_context)
            
            # Chama o Gemini (aqui é onde a mágica acontece!)
            response = await self._call_gemini(system_prompt)
            
            return BotResponse(
                content=response,
                confidence=0.8,  # Por enquanto, valor fixo
                sources=["Gemini 1.5 Flash"]  # Futuramente: documentos PDF
            )
            
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            return BotResponse(
                content="Desculpe, tive um problema técnico. Tente novamente em alguns segundos.",
                error=str(e)
            )
    
    def _build_university_prompt(self, user_message: str, context: Dict[str, Any]) -> str:
        """
        Constrói o prompt otimizado para contexto universitário.
        
        Conceito: Prompt Engineering
        - A qualidade da resposta depende muito de como formulamos a pergunta
        - Contexto específico melhora drasticamente os resultados
        """
        
        base_context = """
Você é o TesseraBot, um assistente virtual especializado em ajudar universitários.

CONTEXTO: Você atende estudantes com dúvidas sobre:
- Matrícula e rematrícula
- Cronogramas acadêmicos
- Editais de bolsas e projetos
- Regulamentos da universidade
- Procedimentos administrativos

INSTRUÇÕES:
- Seja objetivo e direto
- Use linguagem amigável e acessível
- Se não souber a resposta específica, seja honesto
- Sugira onde o estudante pode encontrar informações oficiais
- Sempre mantenha tom helpful e encorajador

PERGUNTA DO ESTUDANTE:
"""
        
        user_info = ""
        if context.get('username'):
            user_info = f"Usuário: {context['username']}\n"
        
        return f"{base_context}\n{user_info}{user_message}"
    
    async def _call_gemini(self, prompt: str) -> str:
        """
        Faz a chamada para a API do Gemini.
        
        Por que método separado?
        - Facilita testing (podemos mockar só esta função)
        - Isola a lógica de API do processamento de negócio
        - Permite retry logic futuro
        """
        
        try:
            print(f"🔍 Chamando Gemini modelo: {self.model.model_name}")
            response = self.model.generate_content(prompt)
            print(f"✅ Resposta recebida: {response.text[:100]}...")
            return response.text.strip()
            
        except Exception as e:
            # Log do erro para debugging
            print(f"❌ Erro na API Gemini: {e}")
            print(f"🔍 Modelo usado: {self.model.model_name}")
            raise  # Re-levanta o erro para ser tratado no nível superior
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status do motor para debugging/monitoramento.
        
        Útil para:
        - Verificar se tudo está funcionando
        - Debugging de problemas
        - Monitoramento de saúde do sistema
        """
        return {
            "initialized": self.is_initialized,
            "bot_name": self.bot_name,
            "has_api_key": bool(self.google_api_key),
            "timestamp": datetime.now().isoformat()
        }

# Instância global do engine (Singleton pattern)
# Por que singleton? 
# - Economiza recursos (só uma conexão com Gemini)
# - Consistência (mesmo estado em toda aplicação)
bot_engine = TesseraBotEngine()