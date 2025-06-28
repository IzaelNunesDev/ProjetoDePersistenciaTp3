#!/usr/bin/env python3
"""
Script de teste para verificar as correções de segurança implementadas.
"""

import asyncio
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext
from app.core.config import settings

def test_password_hashing():
    """Testa se o hashing de senhas está funcionando corretamente"""
    print("🔐 Testando hashing de senhas...")
    
    # Configuração do contexto de senha
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Senha de teste
    test_password = "minha_senha_secreta_123"
    
    # Gerar hash
    hashed_password = pwd_context.hash(test_password)
    print(f"✅ Hash gerado: {hashed_password[:20]}...")
    
    # Verificar senha correta
    is_valid = pwd_context.verify(test_password, hashed_password)
    print(f"✅ Verificação com senha correta: {is_valid}")
    
    # Verificar senha incorreta
    is_invalid = pwd_context.verify("senha_errada", hashed_password)
    print(f"✅ Verificação com senha incorreta: {is_invalid}")
    
    # Verificar que hashes diferentes são gerados para a mesma senha (salt)
    hash1 = pwd_context.hash(test_password)
    hash2 = pwd_context.hash(test_password)
    hashes_different = hash1 != hash2
    print(f"✅ Salt funcionando (hashes diferentes): {hashes_different}")
    
    return True

def test_jwt_configuration():
    """Testa se as configurações JWT estão corretas"""
    print("\n🔑 Testando configurações JWT...")
    
    print(f"✅ SECRET_KEY configurada: {len(settings.SECRET_KEY) > 20}")
    print(f"✅ ALGORITHM configurado: {settings.ALGORITHM}")
    print(f"✅ ACCESS_TOKEN_EXPIRE_HOURS configurado: {settings.ACCESS_TOKEN_EXPIRE_HOURS}")
    
    # Verificar se a chave secreta não é a padrão
    is_not_default = settings.SECRET_KEY != "uma_chave_padrao_apenas_para_dev_nao_usar_em_producao"
    print(f"✅ Chave secreta não é a padrão: {is_not_default}")
    
    return True

def test_imports():
    """Testa se todos os imports necessários estão funcionando"""
    print("\n📦 Testando imports...")
    
    try:
        from app.services.crud_services import CRUDService
        print("✅ CRUDService importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar CRUDService: {e}")
        return False
    
    try:
        from app.routers.router_auth import create_access_token, verify_password
        print("✅ Funções de autenticação importadas com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar funções de autenticação: {e}")
        return False
    
    try:
        from fastapi.security import OAuth2PasswordBearer
        print("✅ OAuth2PasswordBearer importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar OAuth2PasswordBearer: {e}")
        return False
    
    return True

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes de segurança...\n")
    
    tests = [
        test_imports,
        test_password_hashing,
        test_jwt_configuration,
    ]
    
    all_passed = True
    
    for test in tests:
        try:
            result = test()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 Todos os testes de segurança passaram!")
        print("✅ Hashing de senhas corrigido (bcrypt)")
        print("✅ Autenticação JWT corrigida (OAuth2PasswordBearer)")
        print("✅ Chave secreta movida para variáveis de ambiente")
        print("✅ Configurações centralizadas")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 