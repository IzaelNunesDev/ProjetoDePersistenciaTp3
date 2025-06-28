#!/usr/bin/env python3
"""
Test script to check API endpoints and identify issues
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "https://projetodepersistenciatp3.onrender.com/api/v1"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a specific endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\nTesting {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"Method {method} not supported")
            return
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2, default=str)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Timeout error")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    print("Testing RotaFácil API Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/")
    test_endpoint("/health")
    
    # Test routes endpoints
    test_endpoint("/rotas/ativas")
    test_endpoint("/rotas/")
    
    # Test vehicles endpoints
    test_endpoint("/veiculos/")
    
    # Test trips endpoints (this should return 404 for now)
    test_endpoint("/viagens/aluno/test123")
    
    # Test auth endpoints
    test_endpoint("/auth/login", method="POST", data={
        "email": "test@example.com",
        "senha": "password123"
    })

if __name__ == "__main__":
    main() 