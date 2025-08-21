#!/bin/bash

# Railway Deployment Script for Synapse Backend

echo "🚀 Starting Railway Deployment Process"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null
then
    echo "❌ Railway CLI could not be found"
    echo "🔗 Installing Railway CLI..."
    
    # Install Railway CLI
    curl -fsSL https://railway.app/install.sh | sh
    
    # Reload shell
    source ~/.bashrc || source ~/.zshrc || true
fi

echo "✅ Railway CLI is available"

# Login to Railway (will prompt for browser authentication)
echo "🔐 Please authenticate with Railway in your browser"
railway login

# Check if project exists or create new one
echo "📋 Checking for existing Railway project..."

PROJECT_NAME="synapse-backend"

# Try to link to existing project or create new one
echo "🏗️  Creating or linking to Railway project: $PROJECT_NAME"
railway init --name "$PROJECT_NAME" || railway link

# Deploy the application
echo "📦 Deploying application to Railway..."
railway up

echo "✅ Deployment completed!"

# Get the deployed URL
echo "🌐 Getting deployment URL..."
DEPLOY_URL=$(railway url)
echo "🔗 Your application is now available at: $DEPLOY_URL"

echo "📝 To view logs, run: railway logs"
echo "🔄 To redeploy, run this script again"

# Save the URL to a file for easy access
echo "$DEPLOY_URL" > DEPLOYED_URL.txt
echo "💾 Deployment URL saved to DEPLOYED_URL.txt"