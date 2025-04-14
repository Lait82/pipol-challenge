# 📰 Web Scraper con IA + BigQuery (Google Cloud Run Job)

Este proyecto es un challenge que scrapea artículos desde [yogonet.com](https://www.yogonet.com/international), extrae contenido relevante (usando IA o scraping clásico), analiza métricas de texto y las sube a BigQuery.


## 🚀 Features

- ✅ Scraping tradicional con Selenium
- 🤖 Extracción con HuggingFace opcional (AI Based Scraping)
- 📊 Métricas: frecuencia de palabras, caracteres y palabras capitalizadas
- ☁️ Upload automático a BigQuery
- 🐳 Dockerized
- 🔁 Deploy automatizado como Google Cloud Run Job


## 📁 Estructura

```
project/
│
├── main.py                  # Entrada principal del proceso
├── Dockerfile               # Define el contenedor
├── deploy.sh                # Script de deploy a Cloud Run
├── .env                     # Configuración local y de producción
│
├── scraping/                # Lógica de scraping (con IA o no)
├── data_processing/         # Extracción de métricas
├── clients/                 # Cliente de BigQuery
└── loaders/                 # Carga de DataFrames a BigQuery
```


## 🔐 .env de ejemplo

```env
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
GOOGLE_PROJECT_ID=project_name
BIGQUERY_DATASET=news_data
HF_API_KEY=hf_xxx...

REGION=us-central1
REPO_NAME=scrapers
IMAGE_NAME=web-scraper
SERVICE_NAME=web-scraper
TAG=latest
AI_BASED_SCRAPING=false
```

> ☝️ Este archivo se usa tanto localmente como para configurar las variables del entorno en Cloud Run.


## 🧪 Ejecutar localmente

```bash
# Con scraping clásico
python main.py --local

# Con scraping IA + HuggingFace
python main.py --local --ai-based-scraping
```

> El flag `--local` activa el uso de `.env` y los chequeos locales de dependencias.

## 🚀 Deploy a Cloud Run Job

```bash
./deploy.sh
```

Este script hace todo:
1. Carga las variables desde `.env`
2. Buildea la imagen Docker
3. La sube a Artifact Registry
4. Crea o actualiza el Job de Cloud Run
5. Ejecuta el Job automáticamente


## 🪵 Ver logs manualmente

```bash
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=web-scraper" \
  --project=tu-proyecto-id \
  --limit=50 \
  --format="value(textPayload)"
```

## 📌 Requisitos

- Tener configurado Google Cloud CLI (`gcloud`)
- Proyecto con billing activo y servicios habilitados:
  - Artifact Registry
  - Cloud Run
  - BigQuery
- Roles necesarios:
  - `Cloud Run Admin`
  - `Artifact Registry Writer`
  - `BigQuery Data Editor`



# 🧠 Tips
- Para producción si querés usar el el scraping basado en IA usá `AI_BASED_SCRAPING=true` en `.env`



## 📬 Contacto

Cualquier bug, mejora o idea, ¡mandá PR o abrí un issue!