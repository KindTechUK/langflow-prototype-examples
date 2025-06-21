from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Twilio credentials - you'll need to set these as environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio phone number

# API configuration
# This needs to point to where your flow is running on the langflow server locally
API_URL = "http://127.0.0.1:7860/api/v1/run/892d40e3-ed04-44c5-9661-375f3914c349"

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def parse_api_response(response_text):
    """
    Parse the complex API response and extract the message text.
    """
    try:
        response_data = json.loads(response_text)
        
        # Navigate through the nested structure to get the message
        outputs = response_data.get('outputs', [])
        if outputs and len(outputs) > 0:
            first_output = outputs[0]
            outputs_list = first_output.get('outputs', [])
            if outputs_list and len(outputs_list) > 0:
                first_output_item = outputs_list[0]
                results = first_output_item.get('results', {})
                message = results.get('message', {})
                
                # Try to get the text from the message
                if isinstance(message, dict):
                    # Try different possible paths for the text
                    text = (message.get('text') or 
                           message.get('data', {}).get('text') or
                           message.get('artifacts', {}).get('message') or
                           message.get('outputs', {}).get('message', {}).get('message'))
                    
                    if text:
                        return text.strip()
        
        # If we can't find the message in the expected structure, return the raw response
        print(f"Could not parse message from response structure: {response_text[:200]}...")
        return "Sorry, I couldn't process the response properly."
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return "Sorry, there was an error processing the response."
    except Exception as e:
        print(f"Error extracting message: {e}")
        return "Sorry, there was an error processing the response."

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint that receives incoming SMS messages from Twilio.
    Processes the message through the API and sends the response back to the sender.
    """
    # Get the incoming message details
    incoming_message = request.form.get('Body', '')
    sender_phone = request.form.get('From', '')
    
    print(f"Received message from {sender_phone}: {incoming_message}")
    
    # Prepare API request payload
    payload = {
        "input_value": incoming_message,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send API request to process the message
        print(f"Sending API request to: {API_URL}")
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        # Get the processed response
        api_response_text = response.text
        print(f"Raw API Response: {api_response_text[:500]}...")
        
        # Parse the response to extract just the message
        parsed_message = parse_api_response(api_response_text)
        print(f"Parsed message: {parsed_message}")
        
        # Send the parsed message back to the sender
        message = client.messages.create(
            body=parsed_message,
            from_=TWILIO_PHONE_NUMBER,
            to=sender_phone
        )
        
        print(f"Sent parsed message to {sender_phone}: {parsed_message[:100]}...")
        print(f"Message SID: {message.sid}")
        
        # Return empty TwiML response (we're handling the response via API)
        resp = MessagingResponse()
        return str(resp)
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error making API request: {e}"
        print(error_msg)
        
        # Send error message back to user
        try:
            error_response = client.messages.create(
                body="Sorry, I'm having trouble processing your request right now. Please try again later.",
                from_=TWILIO_PHONE_NUMBER,
                to=sender_phone
            )
            print(f"Sent error message to {sender_phone}")
        except Exception as send_error:
            print(f"Error sending error message: {send_error}")
        
        # Return error response
        resp = MessagingResponse()
        resp.message("Sorry, there was an error processing your message.")
        return str(resp)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Return error response
        resp = MessagingResponse()
        resp.message("Sorry, there was an error processing your message.")
        return str(resp)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return {'status': 'healthy', 'service': 'twilio-api-bot'}

if __name__ == '__main__':
    # Check if required environment variables are set
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        print("Error: Missing required environment variables.")
        print("Please set the following environment variables:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN") 
        print("- TWILIO_PHONE_NUMBER")
        exit(1)
    
    print("Starting Twilio API Bot...")
    print(f"Using Twilio phone number: {TWILIO_PHONE_NUMBER}")
    print(f"API endpoint: {API_URL}")
    print("Webhook endpoint: /webhook")
    print("Health check endpoint: /health")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=8888)
