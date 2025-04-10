FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /scraper

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    git \
    wget \
    curl \
    unzip \
    chrome \
    && chromeVersion="$(chrome --version | grep -Eo '([0-9]{1,4}\.){3}[0-9]{1,4}')" \
    && curl -sS -L https://chromedriver.storage.googleapis.com/$chromeVersion/chromedriver_linux64.zip -o chromedriver.zip \
    && unzip chromedriver.zip -d /usr/local/bin/ \
    && rm chromedriver.zip \
    && apt-get install -y \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    libgbm1 \
    xdg-utils \
    && apt-get clean \
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