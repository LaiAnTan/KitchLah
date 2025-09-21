import boto3
import json
from config import Config

def call_bedrock(prompt: str) -> str:
    # Create the client
    bedrock = boto3.client(
        service_name="bedrock-runtime", 
        region_name="us-east-1",
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=Config.AWS_SESSION_TOKEN
     )

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 300,
            "temperature": 0.7,
            "topP": 0.9
        }
    }

    response = bedrock.invoke_model(
        modelId="us.amazon.nova-pro-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )

    output = json.loads(response["body"].read())

    # Nova responses come back as a "messages" array
    # Extract the assistant’s first text message
    try:
        return output["output"]["message"]["content"][0]["text"].strip()
    except Exception:
        return json.dumps(output, indent=2)  # fallback to raw output if parsing fails

