#!/usr/bin/env python3
"""
Setup e test script per sCore Flet
Verifica installazione dipendenze e configurazione
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica versione Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ richiesto")
        return False
    return True

def install_dependencies():
    """Installa dipendenze"""
    print("\n📦 Installazione dipendenze...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dipendenze installate")
        return True
    except subprocess.CalledProcessError:
        print("❌ Errore nell'installazione delle dipendenze")
        return False

def check_secrets():
    """Verifica presenza file secrets"""
    secrets_path = Path(".streamlit/secrets.toml")
    
    if not secrets_path.exists():
        print(f"\n⚠️  File secrets non trovato: {secrets_path}")
        print("\nCrea il file con la seguente struttura:")
        print("""
[strava]
client_id = "TUO_CLIENT_ID"
client_secret = "TUO_CLIENT_SECRET"

[supabase]
url = "TUA_SUPABASE_URL"
key = "TUA_SUPABASE_KEY"

[gemini]
api_key = "TUA_GEMINI_API_KEY"
        """)
        return False
    
    print(f"✓ File secrets trovato: {secrets_path}")
    return True

def test_imports():
    """Testa import dei moduli principali"""
    print("\n🔍 Test imports...")
    
    modules = [
        ("flet", "Flet"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("requests", "Requests"),
    ]
    
    all_ok = True
    for module, name in modules:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ❌ {name} - Installa con: pip install {module}")
            all_ok = False
    
    return all_ok

def run_app():
    """Avvia l'applicazione"""
    print("\n🚀 Avvio applicazione...")
    print("L'app si aprirà in una nuova finestra del browser.\n")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n\n✋ Applicazione fermata dall'utente")
    except Exception as e:
        print(f"\n❌ Errore: {e}")

def main():
    """Main setup e test"""
    print("=" * 60)
    print("🏃‍♂️ sCore 4.0 - Flet Edition - Setup & Test")
    print("=" * 60)
    
    # 1. Check Python
    if not check_python_version():
        sys.exit(1)
    
    # 2. Install deps
    install_dependencies()
    
    # 3. Test imports
    if not test_imports():
        print("\n⚠️  Alcune dipendenze mancano. Installa e riprova.")
        sys.exit(1)
    
    # 4. Check secrets
    has_secrets = check_secrets()
    
    # 5. Summary
    print("\n" + "=" * 60)
    print("📋 RIEPILOGO SETUP")
    print("=" * 60)
    print(f"Python:      ✓")
    print(f"Dipendenze:  ✓")
    print(f"Secrets:     {'✓' if has_secrets else '⚠️  Mancanti'}")
    print("=" * 60)
    
    if has_secrets:
        response = input("\n▶️  Vuoi avviare l'app ora? [Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes', 's', 'si']:
            run_app()
    else:
        print("\n⚠️  Configura i secrets prima di avviare l'app.")
        print("Poi esegui: python main.py")

if __name__ == "__main__":
    main()
