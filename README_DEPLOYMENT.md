# Deploying Synapse Backend to the Cloud

This guide explains how to deploy the Synapse Backend to Render, a free cloud platform.

## Prerequisites

1. A GitHub account
2. A Render account (free)

## Deployment Steps

### 1. Fork the Repository

First, fork this repository to your own GitHub account:
1. Click the "Fork" button at the top right of this repository page
2. Select your GitHub account as the destination

### 2. Create a Render Account

1. Go to [render.com](https://render.com/)
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### 3. Deploy to Render

1. Click the "New+" button on your Render dashboard
2. Select "Web Service"
3. Connect your GitHub account if prompted
4. Select the forked repository
5. Fill in the following details:
   - Name: synapse-backend (or any name you prefer)
   - Region: Choose the one closest to you
   - Branch: main
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
6. Scroll down and click "Create Web Service"

### 4. Wait for Deployment

Render will automatically:
1. Clone your repository
2. Install dependencies
3. Build the application
4. Deploy it

This process may take a few minutes. You'll see the logs in real-time.

### 5. Access Your Deployed Application

Once deployment is complete, you'll see a URL like `https://your-app-name.onrender.com`. This is your public endpoint.

You can test it by visiting:
- `https://your-app-name.onrender.com/` - Main endpoint
- `https://your-app-name.onrender.com/api/personas` - List personas
- `https://your-app-name.onrender.com/health` - Health check

## Environment Variables

If you need to set environment variables (e.g., for API keys):
1. Go to your service dashboard on Render
2. Click "Environment" in the sidebar
3. Add your variables
4. Click "Save Changes" - Render will automatically redeploy

## Notes

- Render's free tier puts services to sleep after 15 minutes of inactivity
- First request after sleep will take longer as the service wakes up
- For production use, consider upgrading to a paid plan for better performance

## Alternative: Railway Deployment

You can also deploy to Railway:
1. Go to [railway.app](https://railway.app/)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Railway will automatically detect it's a Python app and deploy

Railway provides $5 credit for free, with similar sleep behavior for free tier.