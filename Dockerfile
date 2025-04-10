FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /scraper

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requisitos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Establece las variables de entorno para BigQuery (pueden ser sobrescritas en Cloud Run)
# ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
ENV PYTHONUNBUFFERED=TRUE

# Puerto para Cloud Run (aunque no es necesario para jobs, es buena práctica)
EXPOSE 8500

# Comando que se ejecutará al iniciar el contenedor
CMD ["python", "main.py"]