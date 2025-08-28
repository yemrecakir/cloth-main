#!/bin/bash
# Google Cloud Run Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Google Cloud Run Deployment${NC}"
echo "================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI bulunamadı!${NC}"
    echo "Google Cloud SDK'yı yükleyip gcloud auth login yapın"
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Google Cloud projesi seçili değil!${NC}"
    echo "gcloud config set project YOUR_PROJECT_ID komutunu çalıştırın"
    exit 1
fi

echo -e "${YELLOW}📋 Proje: $PROJECT_ID${NC}"

# Build and submit to Cloud Build
echo -e "${YELLOW}🔨 Container build başlatılıyor...${NC}"
gcloud builds submit --config cloudbuild.yaml

# Get service URL
echo -e "${YELLOW}🌐 Servis URL'i alınıyor...${NC}"
SERVICE_URL=$(gcloud run services describe cloth-bg-remover --region=us-central1 --format="value(status.url)")

echo -e "${GREEN}✅ Deployment tamamlandı!${NC}"
echo "🌍 Servis URL: $SERVICE_URL"
echo ""
echo "🧪 Test komutları:"
echo "curl $SERVICE_URL/health"
echo "curl $SERVICE_URL/api/status"

# Health check
echo -e "${YELLOW}🏥 Health check yapılıyor...${NC}"
if curl -f -s "$SERVICE_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Servis sağlıklı çalışıyor!${NC}"
else
    echo -e "${RED}❌ Servis yanıt vermiyor, logları kontrol edin:${NC}"
    echo "gcloud logs read --service=cloth-bg-remover --limit=50"
fi