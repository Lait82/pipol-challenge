#!/bin/bash

set -e

CYAN="\e[36m"
ENDCOLOR="\e[0m"
RED="\e[31m"
GREEN="\e[32m"

# Load env file
if [ -f .env ]; then
  echo -e "${CYAN}📄 Cargando variables desde .env...${ENDCOLOR}"
  export $(grep -v '^#' .env | xargs)
else
  echo -e "${RED}Archivo .env no encontrado. Abortando.${ENDCOLOR}"
  exit 1
fi

ENV_VARS=$(grep -v '^#' .env | xargs | sed 's/ /,/g')

FULL_IMAGE="${REGION}-docker.pkg.dev/${GOOGLE_PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${TAG}"

echo -e "${CYAN}🚧 Building Docker image: ${IMAGE_NAME}:${TAG}"${ENDCOLOR};
docker build -t ${IMAGE_NAME}:${TAG} .;

echo -e "${CYAN}🏷️ Tagging image ${IMAGE_NAME} with tag ${TAG} for Artifact Registry..."${ENDCOLOR};
docker tag ${IMAGE_NAME}:${TAG} ${FULL_IMAGE};

echo -e "${CYAN}🚀 Pushing image to Artifact Registry..."${ENDCOLOR};
docker push ${FULL_IMAGE};

echo -e "${CYAN}☁️ Checking whether ${SERVICE_NAME} exists or not...${ENDCOLOR}"
gcloud run jobs describe ${SERVICE_NAME} \
  --region=${REGION} --project=${GOOGLE_PROJECT_ID} > /dev/null 2>&1 && \
  JOB_EXISTS=true || JOB_EXISTS=false

if $JOB_EXISTS; then
  echo -e "${CYAN}🔄 Updating existing job...${ENDCOLOR}"
  gcloud run jobs update ${SERVICE_NAME} \
    --image=${FULL_IMAGE} \
    --region=${REGION} \
    --memory=1Gi \
    --project=${GOOGLE_PROJECT_ID} \
    --set-env-vars=${ENV_VARS}
else
  echo -e "${CYAN}🆕 Creating new job...${ENDCOLOR}"
  gcloud run jobs create ${SERVICE_NAME} \
    --image=${FULL_IMAGE} \
    --region=${REGION} \
    --memory=1Gi \
    --project=${GOOGLE_PROJECT_ID} \
    --set-env-vars=${ENV_VARS}
fi

echo -e "${CYAN}🏃 Executing job...${ENDCOLOR}"
gcloud run jobs execute ${SERVICE_NAME} \
  --region=${REGION} \
  --project=${GOOGLE_PROJECT_ID}

echo -e "${GREEN}✅ Job executed successfully!${ENDCOLOR}"