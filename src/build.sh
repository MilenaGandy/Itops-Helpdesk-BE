   #!/usr/bin/env bash
    # exit on error
    set -o errexit

    # Usar pip3 para ser explícito
    pip3 install -r requirements.txt

    # Usar python3 para los comandos de manage.py
    python3 manage.py collectstatic --no-input
    python3 manage.py migrate