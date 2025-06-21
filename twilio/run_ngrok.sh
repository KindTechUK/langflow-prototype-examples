#!/bin/bash

# Twilio Lowercase Bot - ngrok tunnel script
# This script starts ngrok to expose your local Flask app to the internet

echo "🚀 Starting ngrok tunnel for Twilio webhook..."
echo "📱 Your Flask app should be running on port 8888"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo "Please install ngrok first: https://ngrok.com/download"
    echo "Or run: brew install ngrok (on macOS)"
    exit 1
fi

# Check if ngrok is authenticated
if [ ! -f ~/.ngrok2/ngrok.yml ]; then
    echo "⚠️  ngrok authentication not found!"
    echo "Please run: ngrok authtoken YOUR_AUTH_TOKEN"
    echo "Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken"
    exit 1
fi

echo "✅ ngrok found and authenticated"
echo "🌐 Starting tunnel on port 8888..."
echo ""

# Start ngrok tunnel
ngrok http 8888

echo ""
echo "📋 Copy the HTTPS URL (e.g., https://abc123.ngrok.io) and add /webhook to it"
echo "🔗 Then set this as your Twilio webhook URL: https://abc123.ngrok.io/webhook" 