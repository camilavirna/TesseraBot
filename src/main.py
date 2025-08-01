"""
TesseraBot - Ponto de Entrada Principal

Este arquivo é o "main" do projeto - onde tudo começa.

Conceitos que você vai aprender:
- Entry point (ponto de entrada)
- Async/await patterns
- Error handling at application level
- Configuration management
"""

import asyncio
import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao Python path para imports funcionarem
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.adapters.discord_adapter import run_discord_bot
from src.core.bot_engine import bot_engine

def check_environment():
    """
    Verifica se o ambiente está configurado corretamente.
    
    Por que fazer essa verificação?
    - Falha rápida: melhor descobrir problemas logo no início
    - User-friendly: mensagens claras sobre o que está faltando
    - Debugging: evita erros confusos mais tarde
    """
    
    print("🔍 Verificando configuração...")
    
    # Verifica se arquivo .env existe
    env_file = project_root / '.env'
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado!")
        print("💡 Crie um arquivo .env baseado no .env.example")
        return False
    
    # Verifica variáveis essenciais
    required_vars = ['DISCORD_BOT_TOKEN', 'GOOGLE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis faltando no .env: {', '.join(missing_vars)}")
        return False
    
    print("✅ Configuração verificada!")
    return True

def show_startup_info():
    """Mostra informações de inicialização."""
    
    print("\n" + "="*50)
    print("🎓 TesseraBot - Assistente Universitário")
    print("="*50)
    print("📋 Funcionalidades:")
    print("   • Responde dúvidas sobre matrícula")
    print("   • Informa sobre cronogramas")
    print("   • Ajuda com editais e regulamentos")
    print("   • Conversa natural no Discord")
    print("\n🔧 Arquitetura Modular:")
    print("   • Core Engine (independente de plataforma)")
    print("   • Discord Adapter (interface Discord)")
    print("   • Preparado para Telegram/Web futuramente")
    print("="*50)

async def main():
    """
    Função principal do TesseraBot.
    
    Por que async?
    - O bot precisa lidar com múltiplas conexões simultâneas
    - APIs modernas são assíncronas
    - Melhor performance e responsividade
    """
    
    show_startup_info()
    
    # 1. Verificar configuração
    if not check_environment():
        print("\n❌ Configuração inválida. Corrija os problemas acima.")
        return 1
    
    # 2. Verificar Core Engine
    print(f"\n🧠 Verificando Core Engine...")
    engine_status = bot_engine.get_status()
    
    if not engine_status['initialized']:
        print("❌ Core Engine não inicializou corretamente")
        print("💡 Verifique sua GOOGLE_API_KEY no arquivo .env")
        return 1
    
    print("✅ Core Engine pronto!")
    
    # 3. Escolher plataforma (futuro: poderá escolher Discord, Telegram, etc.)
    platform = os.getenv('PLATFORM', 'discord').lower()
    
    print(f"\n🚀 Iniciando adapter: {platform}")
    
    if platform == 'discord':
        try:
            await run_discord_bot()
        except KeyboardInterrupt:
            print("\n👋 TesseraBot encerrado pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro crítico: {e}")
            return 1
    else:
        print(f"❌ Plataforma '{platform}' não suportada ainda")
        print("💡 Plataformas disponíveis: discord")
        return 1
    
    return 0

if __name__ == "__main__":
    """
    Entry point do programa.
    
    Por que usar if __name__ == "__main__"?
    - Permite que o arquivo seja importado sem executar automaticamente
    - Boa prática em Python
    - Facilita testing
    """
    
    try:
        # Executa a função principal
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n👋 Tchau!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n💥 Erro não tratado: {e}")
        sys.exit(1)