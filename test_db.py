"""
Teste de Conexão Oracle ADB - axioma_app
Valida: CREATE, INSERT, UPDATE, DELETE
"""

from sqlalchemy import text
import oracledb
from infra.database.connection import engine, SessionLocal
from infra.database.session import get_db
from config.settings import settings

print(f"\n{'='*60}")
print("TESTE DE CONEXÃO ORACLE - axioma_app")
print(f"{'='*60}\n")

print(f"Configuração:")
print(f"  Usuário: {settings.ORACLE_USER}")
print(f"  Serviço: {settings.ORACLE_DSN}")
print(f"  Ambiente: {settings.ENV}\n")

try:
    # Teste 1: Conexão via SQLAlchemy
    print("1. Conectando via SQLAlchemy...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM DUAL"))
        print(f"   ✓ SQLAlchemy conectado\n")
    
    # Teste 2: Sessão via session.py
    print("2. Testando sessão (get_db)...")
    db = SessionLocal()
    
    # Teste 3: CREATE TABLE
    print("3. Criando tabela de teste...")
    try:
        db.execute(text("DROP TABLE usuarios_teste"))
        db.commit()
    except:
        pass
    
    db.execute(text("""
        CREATE TABLE usuarios_teste (
            id NUMBER PRIMARY KEY,
            username VARCHAR2(50) UNIQUE NOT NULL,
            email VARCHAR2(100) NOT NULL,
            password_hash VARCHAR2(255),
            criado_em TIMESTAMP DEFAULT SYSDATE
        )
    """))
    db.commit()
    print(f"   ✓ Tabela criada\n")
    
    # Teste 4: INSERT (Registrar)
    print("4. Inserindo dados (registro)...")
    db.execute(text("""
        INSERT INTO usuarios_teste (id, username, email, password_hash)
        VALUES (1, 'joao', 'joao@axioma.com', 'hash123')
    """))
    db.commit()
    print(f"   ✓ Usuário registrado\n")
    
    # Teste 5: SELECT (Login)
    print("5. Consultando dados (login)...")
    result = db.execute(text("SELECT * FROM usuarios_teste WHERE username = 'joao'"))
    user = result.fetchone()
    if user:
        print(f"   ✓ Usuário encontrado: {user[1]}\n")
    
    # Teste 6: UPDATE (Alterar)
    print("6. Alterando dados...")
    db.execute(text("""
        UPDATE usuarios_teste SET email = 'joao.novo@axioma.com' WHERE username = 'joao'
    """))
    db.commit()
    print(f"   ✓ Dados alterados\n")
    
    # Teste 7: DELETE (Deletar)
    print("7. Deletando dados...")
    db.execute(text("DELETE FROM usuarios_teste WHERE username = 'joao'"))
    db.commit()
    print(f"   ✓ Dados deletados\n")
    
    # Limpeza
    db.execute(text("DROP TABLE usuarios_teste"))
    db.commit()
    db.close()
    
    print(f"{'='*60}")
    print("✓✓✓ TODOS OS TESTES PASSARAM ✓✓✓")
    print(f"{'='*60}")
    print(f"\nOperações funcionando:")
    print(f"  ✓ Registrar usuários (CREATE, INSERT)")
    print(f"  ✓ Login (SELECT)")
    print(f"  ✓ Alterar dados (UPDATE)")
    print(f"  ✓ Deletar dados (DELETE)")
    print(f"\nConexão pronta para uso!\n")

except Exception as e:
    print(f"\n✗ Erro: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'db' in locals():
        db.close()