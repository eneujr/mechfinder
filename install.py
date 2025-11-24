# Script de Instalacao Automatica - MechFinder
# Execute: python install.py

import subprocess
import sys
import os

print("=" * 60)
print("MECHFINDER - INSTALACAO AUTOMATICA")
print("=" * 60)
print()

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"OK - {description} concluido!")
            return True
        else:
            print(f"ERRO - {description} falhou!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"ERRO - {e}")
        return False

# 1. Verificar Python
print("1. VERIFICANDO PYTHON...")
python_version = sys.version
print(f"   Python {python_version}")

# 2. Atualizar pip
run_command(
    f"{sys.executable} -m pip install --upgrade pip",
    "2. Atualizando pip"
)

# 3. Instalar dependencias
print("\n3. INSTALANDO DEPENDENCIAS...")
print("   Isso pode demorar 5-10 minutos na primeira vez...")
run_command(
    f"{sys.executable} -m pip install -r requirements.txt",
    "   Instalando pacotes"
)

# 4. Criar banco de dados
run_command(
    f"{sys.executable} setup_db.py",
    "4. Criando banco de dados"
)

# 5. Aplicar migracoes
run_command(
    f"{sys.executable} migrate_db.py",
    "5. Aplicando migracoes"
)

run_command(
    f"{sys.executable} migrate_image_search.py",
    "   Aplicando migracoes de busca por imagem"
)

# 6. Finalizar
print("\n" + "=" * 60)
print("INSTALACAO CONCLUIDA COM SUCESSO!")
print("=" * 60)
print()
print("Para executar a aplicacao:")
print("   python run.py")
print()
print("Depois acesse no navegador:")
print("   http://localhost:5000")
print()
print("=" * 60)
