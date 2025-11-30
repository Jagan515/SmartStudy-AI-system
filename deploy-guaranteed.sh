#!/bin/bash

echo "🚀 SmartStudy AI - GUARANTEED Deployment"
echo "========================================"

PROJECT_ID="smartstudy-ai-479807"
SERVICE_NAME="smartstudy-ai"
REGION="us-central1"

echo "📋 Project: $PROJECT_ID"
echo "📋 Service: $SERVICE_NAME"

# Step 1: Test locally first
echo ""
echo "🧪 Step 1: Testing server locally..."
python server.py &
SERVER_PID=$!
sleep 3

if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ Local server test PASSED"
    kill $SERVER_PID
else
    echo "❌ Local server test FAILED"
    kill $SERVER_PID
    exit 1
fi

# Step 2: Build for AMD64
echo ""
echo "🔧 Step 2: Building Docker image..."
docker build --platform linux/amd64 -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built"

# Step 3: Push to container registry
echo ""
echo "📤 Step 3: Pushing to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

if [ $? -ne 0 ]; then
    echo "❌ Docker push failed"
    exit 1
fi

echo "✅ Docker image pushed"

# Step 4: Deploy to Cloud Run
echo ""
echo "☁️ Step 4: Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1

if [ $? -ne 0 ]; then
    echo "❌ Cloud Run deployment failed"
    exit 1
fi

# Step 5: Get service URL and test
echo ""
echo "🌐 Step 5: Testing deployment..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format="value(status.url)")

echo "Service URL: $SERVICE_URL"

# Wait a moment for service to be ready
sleep 10

echo ""
echo "🧪 Testing endpoints..."
curl -s "$SERVICE_URL/health"
echo ""
curl -s "$SERVICE_URL/"
echo ""

echo ""
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "🌐 Your SmartStudy AI is live at: $SERVICE_URL"
echo ""
echo "💡 Next: Add your AI features back gradually"