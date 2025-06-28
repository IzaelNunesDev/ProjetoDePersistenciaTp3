#!/usr/bin/env python3
"""
Debug script to help understand 422 validation errors when creating routes.
"""

import requests
import json

# API base URL
BASE_URL = "https://projetodepersistenciatp3.onrender.com/api/v1"

def show_correct_format():
    """Show the correct format for creating routes"""
    
    print("=== FORMATO CORRETO PARA CRIAR ROTAS ===")
    print("""
{
    "nome_rota": "Nome da Rota (1-100 caracteres)",
    "descricao": "Descrição da rota (1-500 caracteres)",
    "turno": "Turno (1-20 caracteres)",
    "ativa": true,
    "pontos_de_parada": [
        {
            "nome_ponto": "Nome do Ponto (1-100 caracteres)",
            "endereco": "Endereço completo (1-200 caracteres)",
            "lat": -23.5505,  // Latitude (-90 a 90)
            "lon": -46.6333,  // Longitude (-180 a 180)
            "ordem": 1        // Ordem (>= 1)
        },
        {
            "nome_ponto": "Segundo Ponto",
            "endereco": "Endereço do segundo ponto",
            "lat": -23.5605,
            "lon": -46.6433,
            "ordem": 2
        }
        // Mínimo 2 pontos de parada
    ]
}
""")

def test_valid_route_creation():
    """Test creating a route with correct format"""
    
    route_data = {
        "nome_rota": "Rota Centro - Campus",
        "descricao": "Rota que conecta o centro da cidade ao campus universitário",
        "turno": "Manhã",
        "ativa": True,
        "pontos_de_parada": [
            {
                "nome_ponto": "Ponto Central",
                "endereco": "Rua das Flores, 123 - Centro",
                "lat": -23.5505,
                "lon": -46.6333,
                "ordem": 1
            },
            {
                "nome_ponto": "Campus Universitário",
                "endereco": "Av. Universitária, 1000 - Campus",
                "lat": -23.5605,
                "lon": -46.6433,
                "ordem": 2
            }
        ]
    }
    
    print("=== Testando criação de rota válida ===")
    print(f"URL: {BASE_URL}/rotas/")
    
    try:
        response = requests.post(
            f"{BASE_URL}/rotas/",
            json=route_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Rota criada com sucesso!")
        else:
            print("❌ Erro na criação da rota")
            print("Resposta:", response.json())
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_invalid_formats():
    """Test various invalid formats"""
    
    print("\n=== Testando formatos inválidos ===")
    
    # Test 1: Missing required fields
    invalid_data_1 = {
        "nome_rota": "Rota Teste",
        "descricao": "Descrição teste"
        # Missing: turno, pontos_de_parada
    }
    
    print("\n1. Dados incompletos:")
    try:
        response = requests.post(f"{BASE_URL}/rotas/", json=invalid_data_1)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Erro de validação capturado")
    except Exception as e:
        print(f"Erro: {e}")
    
    # Test 2: Less than 2 points
    invalid_data_2 = {
        "nome_rota": "Rota Teste",
        "descricao": "Descrição teste",
        "turno": "Manhã",
        "pontos_de_parada": [
            {
                "nome_ponto": "Ponto Único",
                "endereco": "Endereço teste",
                "lat": -23.5505,
                "lon": -46.6333,
                "ordem": 1
            }
        ]
    }
    
    print("\n2. Menos de 2 pontos de parada:")
    try:
        response = requests.post(f"{BASE_URL}/rotas/", json=invalid_data_2)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Erro de validação capturado")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("🚌 Debug da API RotaFácil")
    print("=" * 50)
    
    show_correct_format()
    test_invalid_formats()
    test_valid_route_creation()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print(f"Documentação: {BASE_URL.replace('/api/v1', '')}/docs") 