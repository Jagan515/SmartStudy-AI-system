#!/bin/bash

echo "🚀 SmartStudy AI - Google Cloud Deployment"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from your project root directory"
    exit 1
fi

echo "📦 Step 1: Checking requirements..."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo "✅ requirements.txt found"

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found!"
    exit 1
fi

echo "✅ Dockerfile found"

echo ""
echo "🔧 Step 2: Setting up Google Cloud..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed."
    echo "   Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ Google Cloud SDK is installed"

# Check if user is logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "🔐 Please log in to Google Cloud..."
    gcloud auth login
fi

echo "✅ Logged in to Google Cloud"

echo ""
echo "🌐 Step 3: Creating Google Cloud project..."

# List existing projects
echo "Your current projects:"
gcloud projects list --format="value(projectId)" | head -5

read -p "Enter your PROJECT_ID (or create new in Google Cloud Console): " PROJECT_ID

# Set the project
gcloud config set project $PROJECT_ID

echo "✅ Project set to: $PROJECT_ID"

echo ""
echo "⚙️ Step 4: Enabling required services..."

# Enable required Google Cloud services
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com

echo "✅ Required services enabled"

echo ""
echo "🐳 Step 5: Building and deploying..."

# Build and deploy using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/smartstudy-ai

# Deploy to Cloud Run
gcloud run deploy smartstudy-ai \
    --image gcr.io/$PROJECT_ID/smartstudy-ai \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1

echo ""
echo "🎉 DEPLOYMENT COMPLETED!"
echo "🌐 Your app is now live at the URL above!"
echo ""
echo "💡 Next steps:"
echo "   1. Set your GOOGLE_API_KEY as an environment variable"
echo "   2. Test your deployed application"
echo "   3. Share the URL with others!"