# Twilio API Bot

This is a Flask webhook application that receives SMS messages via Twilio, processes them through a custom API, and sends the response back to the sender.

## Setup Instructions

### 1. Install Dependencies

```bash
# From the project root
pip install flask twilio python-dotenv requests
```

### 2. Set Up Environment Variables

Create a `.env` file in the `twilio/` directory with the following variables:

```env
# Twilio Credentials
# Get these from your Twilio Console: https://console.twilio.com/
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890  # Your Twilio phone number (include country code)
```

### 3. Ensure Your API is Running

Make sure your API server is running on:
```
http://127.0.0.1:7862/api/v1/run/892d40e3-ed04-44c5-9661-375f3914c349
```

The Twilio bot will send incoming SMS messages to this API endpoint for processing.

### 4. Set Up ngrok for Local Development

#### Step 1: Sign up for ngrok
1. Go to [ngrok.com](https://ngrok.com) and click "Sign up for free"
2. Create an account (you can use GitHub, Google, or email)
3. Verify your email address

#### Step 2: Install ngrok
**macOS (using Homebrew):**
```bash
brew install ngrok
```

**macOS (manual install):**
```bash
# Download from https://ngrok.com/download
# Extract and move to /usr/local/bin
```

**Other platforms:**
Download from [ngrok.com/download](https://ngrok.com/download)

#### Step 3: Authenticate ngrok
1. Go to [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
2. Copy your authtoken
3. Run the authentication command:
```bash
ngrok authtoken YOUR_AUTH_TOKEN_HERE
```

#### Step 4: Use the provided script
```bash
# Make the script executable (if not already)
chmod +x run_ngrok.sh

# Run the script
./run_ngrok.sh
```

This will:
- Check if ngrok is installed and authenticated
- Start a tunnel on port 8888
- Display the public URL you need for your Twilio webhook

### 5. Configure Twilio Webhook

1. Go to your [Twilio Console](https://console.twilio.com/)
2. Navigate to Phone Numbers → Manage → Active numbers
3. Click on your phone number
4. In the "Messaging" section, set the webhook URL to:
   ```
   https://your-ngrok-url.ngrok.io/webhook
   ```
   (Replace with the HTTPS URL from ngrok)

### 6. Run the Application

**Terminal 1 - Start the Flask app:**
```bash
cd twilio
python main.py
```

**Terminal 2 - Start ngrok tunnel:**
```bash
cd twilio
./run_ngrok.sh
```

The application will start on `http://localhost:8888` and be accessible via the ngrok URL.

### 7. Test the Application

Send an SMS to your Twilio phone number. The bot will:
1. Receive your message
2. Send it to your API for processing
3. Send the API response back to you

## Manual ngrok Usage (Alternative)

If you prefer to run ngrok manually:

```bash
# Start ngrok tunnel
ngrok http 8888

# Copy the HTTPS URL and add /webhook to it
# Example: https://abc123.ngrok.io/webhook
```

## Endpoints

- `POST /webhook` - Receives incoming SMS messages
- `GET /health` - Health check endpoint

## API Integration

The bot sends incoming SMS messages to your API with this payload:
```json
{
    "input_value": "user's message",
    "output_type": "chat",
    "input_type": "chat"
}
```

The API response is then sent back to the user via SMS.

## Troubleshooting

### ngrok Issues
- **"ngrok command not found"**: Install ngrok first
- **"authentication not found"**: Run `ngrok authtoken YOUR_TOKEN`
- **"tunnel not working"**: Make sure your Flask app is running on port 8888

### Twilio Issues
- **No messages received**: Check that your webhook URL is correct and includes `/webhook`
- **Authentication errors**: Verify your Twilio credentials in the `.env` file
- **Phone number issues**: Ensure your Twilio phone number includes the country code

### API Issues
- **API not responding**: Make sure your API server is running on port 7862
- **API errors**: Check the console logs for detailed error messages
- **Connection refused**: Verify the API URL is correct and accessible

## Features

- ✅ Receives SMS messages via Twilio webhook
- ✅ Processes messages through custom API
- ✅ Sends API response back to sender
- ✅ Error handling and logging
- ✅ Health check endpoint
- ✅ Environment variable configuration
- ✅ Automated ngrok setup script 