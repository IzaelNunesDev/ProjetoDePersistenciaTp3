#!/usr/bin/env python3
"""
Script para iniciar o backend RotaFácil com dados de exemplo
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def install_dependencies():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    return True

def create_sample_data():
    """Cria dados de exemplo no banco MongoDB"""
    print("🗄️ Criando dados de exemplo no MongoDB...")
    
    # Script Python para inserir dados de exemplo no MongoDB
    sample_data_script = """
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('.')))

from app.database import get_database
from app.services.crud_services import (
    create_aluno, create_motorista, create_veiculo, 
    create_rota, create_viagem
)
from app.models.pydantic_models import (
    AlunoCreate, MotoristaCreate, VeiculoCreate, 
    RotaCreate, ViagemCreate
)

async def create_sample_data():
    db = get_database()
    
    # Criar alunos de exemplo
    alunos_data = [
        {
            "nome_completo": "João Silva",
            "email": "joao@email.com",
            "senha": "test123",
            "matricula": "2024001",
            "telefone": "(11) 99999-1111"
        },
        {
            "nome_completo": "Maria Santos",
            "email": "maria@email.com",
            "senha": "test123",
            "matricula": "2024002",
            "telefone": "(11) 99999-2222"
        },
        {
            "nome_completo": "Pedro Oliveira",
            "email": "pedro@email.com",
            "senha": "test123",
            "matricula": "2024003",
            "telefone": "(11) 99999-3333"
        }
    ]
    
    # Criar motoristas de exemplo
    motoristas_data = [
        {
            "nome_completo": "Carlos Motorista",
            "email": "carlos@email.com",
            "senha": "test123",
            "cnh": "12345678901",
            "data_admissao": "2024-01-15",
            "status_ativo": True
        },
        {
            "nome_completo": "Ana Condutora",
            "email": "ana@email.com",
            "senha": "test123",
            "cnh": "98765432109",
            "data_admissao": "2024-02-01",
            "status_ativo": True
        }
    ]
    
    # Criar veículos de exemplo
    veiculos_data = [
        {
            "placa": "ABC-1234",
            "modelo": "Mercedes-Benz Sprinter",
            "capacidade_passageiros": 15,
            "status_manutencao": "Disponível",
            "adaptado_pcd": False,
            "ano_fabricacao": 2020
        },
        {
            "placa": "DEF-5678",
            "modelo": "Volkswagen Kombi",
            "capacidade_passageiros": 12,
            "status_manutencao": "Disponível",
            "adaptado_pcd": True,
            "ano_fabricacao": 2019
        }
    ]
    
    # Criar rotas de exemplo
    rotas_data = [
        {
            "nome_rota": "Rota Centro - Manhã",
            "descricao": "Rota do centro da cidade para o período matutino",
            "turno": "Manhã",
            "ativa": True
        },
        {
            "nome_rota": "Rota Norte - Tarde",
            "descricao": "Rota da zona norte para o período vespertino",
            "turno": "Tarde",
            "ativa": True
        }
    ]
    
    try:
        # Inserir alunos
        for aluno_data in alunos_data:
            await create_aluno(AlunoCreate(**aluno_data))
        
        # Inserir motoristas
        for motorista_data in motoristas_data:
            await create_motorista(MotoristaCreate(**motorista_data))
        
        # Inserir veículos
        for veiculo_data in veiculos_data:
            await create_veiculo(VeiculoCreate(**veiculo_data))
        
        # Inserir rotas
        for rota_data in rotas_data:
            await create_rota(RotaCreate(**rota_data))
        
        print('Dados de exemplo criados com sucesso no MongoDB!')
        
    except Exception as e:
        print(f'Erro ao criar dados de exemplo: {e}')

# Executar a função
import asyncio
asyncio.run(create_sample_data())
    """
    
    try:
        # Executar o script Python
        subprocess.run([sys.executable, "-c", sample_data_script], check=True)
        print("✅ Dados de exemplo criados com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
        return False
    return True

def start_server():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando servidor FastAPI...")
    print("📡 Servidor rodando em: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("\n👥 Dados de exemplo criados:")
    print("   Alunos: joao@email.com, maria@email.com, pedro@email.com")
    print("   Motoristas: carlos@email.com, ana@email.com")
    print("   Senha para todos: test123")
    print("\n⏹️  Pressione Ctrl+C para parar o servidor")
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar servidor: {e}")

def main():
    """Função principal"""
    print("🚌 RotaFácil Backend (MongoDB)")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("main.py").exists():
        print("❌ Execute este script no diretório ProjetoDePersistencia")
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        sys.exit(1)
    
    # Criar dados de exemplo
    if not create_sample_data():
        sys.exit(1)
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main() 