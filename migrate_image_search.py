# -*- coding: utf-8 -*-
"""
Script de migracao para adicionar tabelas de busca por imagem
"""

from app import create_app
from app.models import db, ImageSearch, ProductFeatures

app = create_app()

with app.app_context():
    print("Criando novas tabelas para busca por imagem...")
    
    try:
        # Criar tabelas
        db.create_all()
        print("OK - Tabelas criadas com sucesso!")
        print("   - ImageSearch (historico de buscas)")
        print("   - ProductFeatures (cache de features)")
        
    except Exception as e:
        print(f"ERRO ao criar tabelas: {e}")

print("\nMigracao concluida!")
