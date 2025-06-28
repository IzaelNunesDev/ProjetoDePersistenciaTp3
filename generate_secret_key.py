import secrets
import string

def generate_secret_key(length: int = 64) -> str:
    """Gera uma chave secreta segura para JWT"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(f"Chave secreta gerada: {secret_key}")
    print("\nCopie esta chave para o arquivo config.env:")
    print(f"SECRET_KEY={secret_key}") 