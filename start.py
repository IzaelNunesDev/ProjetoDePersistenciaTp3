#!/usr/bin/env python3
"""
Script de inicialização da API RotaFácil
Este script verifica as dependências e inicia a aplicação
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 9):
        print("❌ Erro: Python 3.9 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_mongodb():
    """Verifica se o MongoDB está disponível"""
    try:
        import motor
        print("✅ Motor (MongoDB driver) disponível")
        return True
    except ImportError:
        print("❌ Motor não encontrado. Execute: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Instala as dependências se necessário"""
    if not os.path.exists("venv"):
        print("📦 Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Ambiente virtual criado")
    
    # Ativa o ambiente virtual
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Linux/Mac
        activate_script = "venv/bin/activate"
    
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def check_config():
    """Verifica se o arquivo de configuração existe"""
    if not os.path.exists("config.env"):
        print("❌ Arquivo config.env não encontrado")
        print("📝 Criando arquivo de configuração padrão...")
        
        config_content = """MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=rotafacil"""
        
        with open("config.env", "w") as f:
            f.write(config_content)
        print("✅ Arquivo config.env criado")
    
    print("✅ Configuração verificada")

def start_application():
    """Inicia a aplicação"""
    print("\n🚀 Iniciando API RotaFácil...")
    print("📖 Documentação disponível em: http://localhost:8000/docs")
    print("🔍 ReDoc disponível em: http://localhost:8000/redoc")
    print("🏥 Health check: http://localhost:8000/health")
    print("\nPressione Ctrl+C para parar a aplicação\n")
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")

def main():
    """Função principal"""
    print("=" * 60)
    print("🚌 RotaFácil API - Sistema de Gerenciamento de Transporte")
    print("=" * 60)
    
    # Verificações iniciais
    if not check_python_version():
        sys.exit(1)
    
    check_config()
    
    # Instala dependências se necessário
    if not check_mongodb():
        if not install_dependencies():
            sys.exit(1)
    
    print("\n✅ Todas as verificações passaram!")
    print("\n💡 Dicas:")
    print("   - Certifique-se de que o MongoDB está rodando")
    print("   - Use 'python exemplos_uso.py' para testar a API")
    print("   - Acesse http://localhost:8000/docs para a documentação interativa")
    
    # Pergunta se deve iniciar a aplicação
    response = input("\n🎯 Deseja iniciar a aplicação agora? (s/n): ").lower().strip()
    if response in ['s', 'sim', 'y', 'yes']:
        start_application()
    else:
        print("\n📝 Para iniciar manualmente, execute: python main.py")

if __name__ == "__main__":
    main() 