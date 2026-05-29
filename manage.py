"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / '.env')
    env_path = BASE_DIR / '.env'
    print(f"📁 Buscando .env en: {env_path}")
    print(f"✅ Existe: {env_path.exists()}")
    result = load_dotenv(env_path, override=True)  # ← agrega override=True
    print(f"📧 Cargado: {result}")
    print(f"📧 EMAIL: {os.environ.get('EMAIL_HOST_USER')}")
    print(f"📧 PASSWORD: {os.environ.get('EMAIL_HOST_PASSWORD')}")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ms_certificates.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()