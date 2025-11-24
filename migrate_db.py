# -*- coding: utf-8 -*-
"""
Script para adicionar as colunas 'number' e 'cep' à tabela Store
Execute este script para atualizar o banco de dados existente
"""
from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    # Adicionar colunas se não existirem
    try:
        # Verificar se as colunas já existem
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('store')]
        
        if 'number' not in columns or 'cep' not in columns:
            print("Adicionando novas colunas a tabela Store...")
            
            # Adicionar colunas usando SQL direto
            with db.engine.connect() as conn:
                if 'number' not in columns:
                    conn.execute(db.text("ALTER TABLE store ADD COLUMN number VARCHAR(20)"))
                    print("OK - Coluna 'number' adicionada")
                
                if 'cep' not in columns:
                    conn.execute(db.text("ALTER TABLE store ADD COLUMN cep VARCHAR(10)"))
                    print("OK - Coluna 'cep' adicionada")
                
                conn.commit()
            
            print("\nSUCESSO - Banco de dados atualizado!")
        else:
            print("OK - Colunas 'number' e 'cep' ja existem no banco de dados")
            
    except Exception as e:
        print(f"ERRO ao atualizar banco de dados: {e}")
        print("\nSe o erro persistir, voce pode:")
        print("1. Deletar o arquivo instance/mechfinder.db")
        print("2. Executar python setup_db.py novamente")
