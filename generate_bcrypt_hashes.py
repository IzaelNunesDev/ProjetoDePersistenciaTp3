#!/usr/bin/env python3
"""
Script para gerar hashes bcrypt para as senhas de exemplo
"""

from passlib.context import CryptContext

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hash(password: str) -> str:
    """Gera hash bcrypt para uma senha"""
    return pwd_context.hash(password)

if __name__ == "__main__":
    password = "test123"
    hash_result = generate_hash(password)
    print(f"Senha: {password}")
    print(f"Hash bcrypt: {hash_result}")
    
    # Verificar se o hash está correto
    is_valid = pwd_context.verify(password, hash_result)
    print(f"Hash válido: {is_valid}") 