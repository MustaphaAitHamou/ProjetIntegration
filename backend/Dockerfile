# backend/Dockerfile
FROM python:3.11-slim

# 1) Variables d’env : pour que pytest trouve app.py
ENV PYTHONPATH=/app

# 2) Dépendances système pour mysqlclient
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      default-libmysqlclient-dev \
      pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3) Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copie du code
COPY . .

# 5) Déclaration du dossier de tests (optionnel)
# Permet à pytest de savoir où chercher ; sinon pytest détectera quand même /app/tests
# Créé un fichier pytest.ini dans /app :
# -----------------
# [pytest]
# testpaths = tests
# python_files = test_*.py
# -----------------

# 6) Démarrage de l’API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
