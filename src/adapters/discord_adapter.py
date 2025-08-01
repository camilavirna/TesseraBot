"""
Discord Adapter - Interface entre Discord e o Core Engine

Este arquivo é responsável APENAS por:
1. Conectar com Discord
2. Receber mensagens
3. Enviar para o Core Engine
4. Retornar respostas para o Discord

Conceitos que você vai aprender:
- Adapter Pattern (padrão adaptador)
- Event-driven programming (programação orientada a eventos)
- API integration (integração com APIs externas)
"""

import os
import asyncio
from typing import Optional
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Importa nosso Core Engine (independente de plataforma)
from src.core.bot_engine import bot_engine, BotResponse

# Carrega configurações
load_dotenv()

class TesseraDiscordBot:
    """
    Adapter para Discord que usa o TesseraBotEngine.
    
    Por que separar isso do Core Engine?
    - O Core Engine pode ser usado em outras plataformas (Telegram, Web)
    - Facilita testing (podemos testar o core sem Discord)
    - Single Responsibility Principle: cada classe tem UMA responsabilidade
    
    Responsabilidade desta classe:
    - Conectar com Discord ✓
    - Tratar eventos do Discord ✓ 
    - Formatar mensagens para o Discord ✓
    - NÃO processar IA (isso é do Core Engine)
    """
    
    def __init__(self):
        """Inicializa o bot Discord."""
        
        # Configurações do Discord
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')
        self.bot_prefix = os.getenv('BOT_PREFIX', '!')
        
        if not self.discord_token:
            raise ValueError("❌ DISCORD_BOT_TOKEN não encontrado no arquivo .env")
        
        # Configura intents (permissões) do Discord
        # Intents = o que o bot pode "ver" no servidor
        intents = discord.Intents.default()
        intents.message_content = True  # Necessário para ler mensagens (novo no Discord)
        
        # Cria o cliente Discord
        self.bot = commands.Bot(
            command_prefix=self.bot_prefix,
            intents=intents,
            help_command=None  # Vamos criar nosso próprio help
        )
        
        # Registra eventos
        self._setup_events()
        self._setup_commands()
        
        print(f"✅ Discord Adapter configurado (prefix: {self.bot_prefix})")
    
    def _setup_events(self):
        """
        Configura eventos do Discord.
        
        Conceito: Event-driven programming
        - O bot "escuta" eventos que acontecem no Discord
        - Quando algo acontece (mensagem, usuário entrou, etc), uma função é chamada
        """
        
        @self.bot.event
        async def on_ready():
            """Executado quando o bot conecta com sucesso."""
            print(f"🤖 {self.bot.user} conectado ao Discord!")
            print(f"📊 Conectado a {len(self.bot.guilds)} servidor(es)")
            
            # Define status do bot
            activity = discord.Activity(
                type=discord.ActivityType.listening,
                name="dúvidas universitárias | !help"
            )
            await self.bot.change_presence(activity=activity)
        
        @self.bot.event
        async def on_message(message):
            """
            Executado toda vez que uma mensagem é enviada.
            
            Args:
                message: Objeto Message do Discord com todos os dados
            """
            
            print(f"📩 Mensagem recebida: '{message.content}' de {message.author}")
            
            # Ignora mensagens do próprio bot (evita loops infinitos!)
            if message.author == self.bot.user:
                print("🚫 Ignorando mensagem do próprio bot")
                return
            
            # Ignora bots (opcional)
            if message.author.bot:
                print("🚫 Ignorando mensagem de outro bot")
                return
            
            # Se a mensagem menciona o bot OU começa com o prefix
            is_mention = self.bot.user.mentioned_in(message)
            is_command = message.content.startswith(self.bot_prefix)
            is_dm = isinstance(message.channel, discord.DMChannel)
            
            # Verifica se menciona o bot de outras formas
            bot_mentioned_text = f"<@{self.bot.user.id}>" in message.content
            tesserabot_mentioned = "tesserabot" in message.content.lower()
            
            print(f"🔍 Análise detalhada:")
            print(f"  - is_mention: {is_mention}")
            print(f"  - is_command: {is_command}")
            print(f"  - is_dm: {is_dm}")
            print(f"  - bot_mentioned_text: {bot_mentioned_text}")
            print(f"  - tesserabot_mentioned: {tesserabot_mentioned}")
            print(f"  - message.content: '{message.content}'")
            
            # Processa mensagem natural (sem comandos)
            if is_mention or is_dm or tesserabot_mentioned or bot_mentioned_text:
                print("💬 Processando como mensagem natural")
                await self._handle_natural_message(message)
                return
            
            # Processa comandos normalmente
            print("⚡ Processando como comando")
            await self.bot.process_commands(message)
        
        @self.bot.event
        async def on_command_error(ctx, error):
            """Trata erros de comandos."""
            if isinstance(error, commands.CommandNotFound):
                await ctx.send("🤔 Comando não encontrado. Use `!help` para ver comandos disponíveis.")
            else:
                print(f"❌ Erro no comando: {error}")
                await ctx.send("😅 Ops! Algo deu errado. Tente novamente.")
    
    def _setup_commands(self):
        """
        Define comandos específicos do Discord.
        
        Conceito: Command Pattern
        - Encapsula ações em objetos/funções
        - Facilita adicionar novos comandos
        - Permite undo/redo futuramente
        """
        
        @self.bot.command(name='status')
        async def status_command(ctx):
            """Mostra status do bot."""
            
            engine_status = bot_engine.get_status()
            
            embed = discord.Embed(
                title="📊 Status do TesseraBot",
                color=0x00ff00 if engine_status['initialized'] else 0xff0000
            )
            
            embed.add_field(
                name="Core Engine", 
                value="✅ Online" if engine_status['initialized'] else "❌ Offline",
                inline=True
            )
            
            embed.add_field(
                name="API Gemini",
                value="✅ Conectada" if engine_status['has_api_key'] else "❌ Sem chave",
                inline=True
            )
            
            embed.add_field(
                name="Servidores",
                value=f"{len(self.bot.guilds)}",
                inline=True
            )
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name='help', aliases=['ajuda'])
        async def help_command(ctx):
            """Mostra comandos disponíveis."""
            
            embed = discord.Embed(
                title="🎓 TesseraBot - Assistente Universitário",
                description="Sou seu assistente para dúvidas universitárias!",
                color=0x3498db
            )
            
            embed.add_field(
                name="💬 Conversa Natural",
                value="Me mencione (@TesseraBot) ou mande DM\n"
                      "Exemplo: `@TesseraBot qual a data da matrícula?`",
                inline=False
            )
            
            embed.add_field(
                name="🛠️ Comandos",
                value="`!status` - Ver status do bot\n"
                      "`!help` - Mostrar esta ajuda",
                inline=False
            )
            
            embed.add_field(
                name="📚 O que posso ajudar",
                value="• Datas de matrícula\n"
                      "• Documentos necessários\n"
                      "• Editais de bolsas\n"
                      "• Cronogramas acadêmicos\n"
                      "• Regulamentos",
                inline=False
            )
            
            embed.set_footer(text="TesseraBot v1.0 - Desenvolvido para ajudar universitários")
            
            await ctx.send(embed=embed)
        
        @self.bot.command(name='test', aliases=['teste'])
        async def test_command(ctx, *, message="Olá! Como você pode me ajudar?"):
            """Testa o Core Engine."""
            
            print(f"🧪 Comando test executado: '{message}'")
            
            # Mostra que está processando
            async with ctx.typing():
                response = await self._process_with_engine(message, ctx.author)
            
            await self._send_response(ctx.send, response)
        
        @self.bot.command(name='debug')
        async def debug_command(ctx):
            """Comando de debug para testar detecção."""
            
            embed = discord.Embed(title="🔍 Debug Info", color=0x00ff00)
            embed.add_field(name="Bot User", value=f"{self.bot.user}", inline=False)
            embed.add_field(name="Bot ID", value=f"{self.bot.user.id}", inline=False)
            embed.add_field(name="Prefix", value=f"{self.bot_prefix}", inline=False)
            
            await ctx.send(embed=embed)
    
    async def _handle_natural_message(self, message):
        """
        Processa mensagem natural (sem comando).
        
        Args:
            message: Objeto Message do Discord
        """
        
        # Remove menções do texto para ficar mais limpo
        clean_content = message.clean_content
        if clean_content.lower().startswith('tesserabot'):
            clean_content = clean_content[10:].strip()  # Remove "tesserabot"
        
        # Mostra que está "pensando" (boa UX!)
        async with message.channel.typing():
            response = await self._process_with_engine(clean_content, message.author)
        
        await self._send_response(message.channel.send, response)
    
    async def _process_with_engine(self, text: str, author) -> BotResponse:
        """
        Processa texto usando o Core Engine.
        
        Esta é a ponte entre Discord e nosso Core Engine!
        """
        
        user_context = {
            'username': author.display_name,
            'user_id': str(author.id),
            'platform': 'discord'
        }
        
        # Aqui é onde a mágica acontece: chama o Core Engine!
        return await bot_engine.process_message(text, user_context)
    
    async def _send_response(self, send_func, response: BotResponse):
        """
        Envia resposta formatada para o Discord.
        
        Args:
            send_func: Função para enviar (channel.send ou ctx.send)
            response: Resposta do Core Engine
        """
        
        if response.error:
            # Se houve erro, envia mensagem de erro amigável
            embed = discord.Embed(
                title="❌ Erro",
                description=response.content,
                color=0xff0000
            )
            await send_func(embed=embed)
            return
        
        # Resposta normal
        embed = discord.Embed(
            description=response.content,
            color=0x3498db,
            timestamp=response.timestamp
        )
        
        # Adiciona fontes se existirem
        if response.sources:
            embed.set_footer(text=f"Fontes: {', '.join(response.sources)}")
        
        await send_func(embed=embed)
    
    async def start(self):
        """Inicia o bot Discord."""
        try:
            print("🚀 Iniciando TesseraBot...")
            await self.bot.start(self.discord_token)
        except Exception as e:
            print(f"❌ Erro ao iniciar bot Discord: {e}")
            raise
    
    async def stop(self):
        """Para o bot Discord."""
        await self.bot.close()
        print("🛑 Bot Discord desconectado")

# Função para executar o bot (será chamada do main.py)
async def run_discord_bot():
    """Função principal para executar o bot Discord."""
    
    discord_bot = TesseraDiscordBot()
    
    try:
        await discord_bot.start()
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
        await discord_bot.stop()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        await discord_bot.stop()
        raise