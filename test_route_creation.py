#!/usr/bin/env python3
"""
Test script to demonstrate correct route creation format
and help debug 422 validation errors.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "https://projetodepersistenciatp3.onrender.com/api/v1"

def test_route_creation():
    """Test creating a route with correct format"""
    
    # Example route data with correct format
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
            },
            {
                "nome_ponto": "Terminal de Ônibus",
                "endereco": "Rua do Terminal, 500 - Centro",
                "lat": -23.5405,
                "lon": -46.6233,
                "ordem": 3
            }
        ]
    }
    
    print("=== Testando criação de rota ===")
    print(f"URL: {BASE_URL}/rotas/")
    print(f"Dados enviados:")
    print(json.dumps(route_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/rotas/",
            json=route_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Rota criada com sucesso!")
            print("Resposta:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("❌ Erro na criação da rota")
            print("Resposta:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_invalid_route_formats():
    """Test various invalid formats to show common mistakes"""
    
    print("\n=== Testando formatos inválidos ===")
    
    # Test 1: Missing required fields
    invalid_data_1 = {
        "nome_rota": "Rota Teste",
        "descricao": "Descrição teste"
        # Missing: turno, pontos_de_parada
    }
    
    print("\n1. Testando dados incompletos (faltando campos obrigatórios):")
    print(json.dumps(invalid_data_1, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(f"{BASE_URL}/rotas/", json=invalid_data_1)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Erro de validação capturado corretamente")
            print("Detalhes:", response.json())
    except Exception as e:
        print(f"Erro: {e}")
    
    # Test 2: Invalid coordinates
    invalid_data_2 = {
        "nome_rota": "Rota Teste",
        "descricao": "Descrição teste",
        "turno": "Manhã",
        "pontos_de_parada": [
            {
                "nome_ponto": "Ponto Teste",
                "endereco": "Endereço teste",
                "lat": 200.0,  # Invalid latitude (> 90)
                "lon": -46.6333,
                "ordem": 1
            }
        ]
    }
    
    print("\n2. Testando coordenadas inválidas:")
    print(json.dumps(invalid_data_2, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(f"{BASE_URL}/rotas/", json=invalid_data_2)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Erro de validação capturado corretamente")
            print("Detalhes:", response.json())
    except Exception as e:
        print(f"Erro: {e}")
    
    # Test 3: Less than 2 points
    invalid_data_3 = {
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
    
    print("\n3. Testando menos de 2 pontos de parada:")
    print(json.dumps(invalid_data_3, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(f"{BASE_URL}/rotas/", json=invalid_data_3)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Erro de validação capturado corretamente")
            print("Detalhes:", response.json())
    except Exception as e:
        print(f"Erro: {e}")

def show_correct_format():
    """Show the correct format for creating routes"""
    
    print("\n=== FORMATO CORRETO PARA CRIAR ROTAS ===")
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

def test_existing_routes():
    """Test getting existing routes"""
    
    print("\n=== Testando listagem de rotas existentes ===")
    
    try:
        # Get all routes
        response = requests.get(f"{BASE_URL}/rotas/")
        print(f"Todas as rotas - Status: {response.status_code}")
        if response.status_code == 200:
            routes = response.json()
            print(f"Total de rotas: {len(routes)}")
            for route in routes[:3]:  # Show first 3
                print(f"- {route.get('nome_rota', 'N/A')} ({route.get('turno', 'N/A')})")
        
        # Get active routes
        response = requests.get(f"{BASE_URL}/rotas/ativas")
        print(f"\nRotas ativas - Status: {response.status_code}")
        if response.status_code == 200:
            active_routes = response.json()
            print(f"Total de rotas ativas: {len(active_routes)}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("🚌 Teste da API RotaFácil")
    print("=" * 50)
    
    # Show correct format first
    show_correct_format()
    
    # Test existing routes
    test_existing_routes()
    
    # Test invalid formats
    test_invalid_route_formats()
    
    # Test valid route creation
    test_route_creation()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")
    print("\nPara mais informações, consulte:")
    print(f"- Documentação da API: {BASE_URL.replace('/api/v1', '')}/docs")
    print(f"- Redoc: {BASE_URL.replace('/api/v1', '')}/redoc") 