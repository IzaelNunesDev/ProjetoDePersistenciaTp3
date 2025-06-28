"""
Exemplos de uso da API RotaFácil
Este arquivo contém exemplos de como usar a API para testar todas as funcionalidades
"""

import requests
import json
from datetime import datetime, date

# Configuração base
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}

def print_response(response, title):
    """Função auxiliar para imprimir respostas"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_health_check():
    """Teste de health check"""
    response = requests.get("http://localhost:8000/health")
    print_response(response, "Health Check")

def test_criar_veiculo():
    """Exemplo: Criar um veículo"""
    veiculo_data = {
        "placa": "ABC1234",
        "modelo": "Ônibus Escolar",
        "capacidade_passageiros": 30,
        "status_manutencao": "Disponível",
        "adaptado_pcd": False,
        "ano_fabricacao": 2020
    }
    
    response = requests.post(f"{BASE_URL}/veiculos/", 
                           headers=HEADERS, 
                           data=json.dumps(veiculo_data))
    print_response(response, "Criar Veículo")
    return response.json().get("id") if response.status_code == 201 else None

def test_criar_motorista():
    """Exemplo: Criar um motorista"""
    motorista_data = {
        "nome_completo": "João Silva",
        "email": "joao.silva@email.com",
        "senha": "123456",
        "cnh": "12345678901",
        "data_admissao": "2023-01-15",
        "status_ativo": True
    }
    
    response = requests.post(f"{BASE_URL}/motoristas/", 
                           headers=HEADERS, 
                           data=json.dumps(motorista_data))
    print_response(response, "Criar Motorista")
    return response.json().get("id") if response.status_code == 201 else None

def test_criar_rota():
    """Exemplo: Criar uma rota"""
    rota_data = {
        "nome_rota": "Rota Centro",
        "descricao": "Rota que atende o centro da cidade",
        "turno": "Manhã",
        "ativa": True,
        "pontos_de_parada": [
            {
                "nome_ponto": "Ponto Central",
                "endereco": "Rua Principal, 123",
                "lat": -3.1190,
                "lon": -60.0217,
                "ordem": 1
            },
            {
                "nome_ponto": "Escola",
                "endereco": "Av. Educação, 456",
                "lat": -3.1200,
                "lon": -60.0220,
                "ordem": 2
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rotas/", 
                           headers=HEADERS, 
                           data=json.dumps(rota_data))
    print_response(response, "Criar Rota")
    return response.json().get("id") if response.status_code == 201 else None

def test_criar_aluno():
    """Exemplo: Criar um aluno"""
    aluno_data = {
        "nome_completo": "Maria Santos",
        "email": "maria.santos@email.com",
        "senha": "123456",
        "matricula": "2024001",
        "telefone": "(11) 99999-9999",
        "necessidade_especial": None
    }
    
    response = requests.post(f"{BASE_URL}/alunos/", 
                           headers=HEADERS, 
                           data=json.dumps(aluno_data))
    print_response(response, "Criar Aluno")
    return response.json().get("id") if response.status_code == 201 else None

def test_criar_viagem(rota_id, motorista_id, veiculo_id):
    """Exemplo: Criar uma viagem"""
    viagem_data = {
        "data_viagem": date.today().isoformat(),
        "status": "Agendada",
        "rota_id": rota_id,
        "motorista_id": motorista_id,
        "veiculo_id": veiculo_id,
        "incidentes": []
    }
    
    response = requests.post(f"{BASE_URL}/viagens/", 
                           headers=HEADERS, 
                           data=json.dumps(viagem_data))
    print_response(response, "Criar Viagem")
    return response.json().get("id") if response.status_code == 201 else None

def test_listar_veiculos():
    """Exemplo: Listar veículos"""
    response = requests.get(f"{BASE_URL}/veiculos/")
    print_response(response, "Listar Veículos")

def test_buscar_veiculos():
    """Exemplo: Buscar veículos por filtros"""
    response = requests.get(f"{BASE_URL}/veiculos/buscar/?status_manutencao=Disponível")
    print_response(response, "Buscar Veículos Disponíveis")

def test_veiculos_disponiveis():
    """Exemplo: Listar veículos disponíveis"""
    response = requests.get(f"{BASE_URL}/veiculos/disponiveis/")
    print_response(response, "Veículos Disponíveis")

def test_estatisticas_veiculos():
    """Exemplo: Estatísticas de veículos"""
    response = requests.get(f"{BASE_URL}/veiculos/estatisticas/")
    print_response(response, "Estatísticas de Veículos")

def test_viagem_detalhada(viagem_id):
    """Exemplo: Consulta complexa - Viagem detalhada"""
    response = requests.get(f"{BASE_URL}/viagens/{viagem_id}/detalhes")
    print_response(response, "Viagem Detalhada")

def test_alunos_viagem(viagem_id):
    """Exemplo: Consulta complexa - Alunos de uma viagem"""
    response = requests.get(f"{BASE_URL}/viagens/{viagem_id}/alunos")
    print_response(response, "Alunos da Viagem")

def test_estatisticas_periodo():
    """Exemplo: Estatísticas por período"""
    data_inicio = "2024-01-01"
    data_fim = "2024-12-31"
    response = requests.get(f"{BASE_URL}/viagens/estatisticas/periodo/?data_inicio={data_inicio}&data_fim={data_fim}")
    print_response(response, "Estatísticas por Período")

def test_paginacao():
    """Exemplo: Paginação"""
    response = requests.get(f"{BASE_URL}/veiculos/pagina/?page=0&limit=5")
    print_response(response, "Paginação de Veículos")

def test_contar_entidades():
    """Exemplo: Contar entidades"""
    response = requests.get(f"{BASE_URL}/veiculos/quantidade/total")
    print_response(response, "Contar Veículos")

def test_buscar_por_texto():
    """Exemplo: Busca por texto"""
    response = requests.get(f"{BASE_URL}/veiculos/buscar/texto/?texto=ABC")
    print_response(response, "Busca por Texto")

def main():
    """Função principal para executar todos os testes"""
    print("🚀 Iniciando testes da API RotaFácil")
    
    # Teste de health check
    test_health_check()
    
    # Criar entidades
    veiculo_id = test_criar_veiculo()
    motorista_id = test_criar_motorista()
    rota_id = test_criar_rota()
    aluno_id = test_criar_aluno()
    
    if all([veiculo_id, motorista_id, rota_id]):
        viagem_id = test_criar_viagem(rota_id, motorista_id, veiculo_id)
        
        if viagem_id:
            # Testes de consultas complexas
            test_viagem_detalhada(viagem_id)
            test_alunos_viagem(viagem_id)
    
    # Testes gerais
    test_listar_veiculos()
    test_buscar_veiculos()
    test_veiculos_disponiveis()
    test_estatisticas_veiculos()
    test_estatisticas_periodo()
    test_paginacao()
    test_contar_entidades()
    test_buscar_por_texto()
    
    print("\n✅ Testes concluídos!")

if __name__ == "__main__":
    main() 