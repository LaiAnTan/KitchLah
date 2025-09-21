import boto3
import json

# Create the client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

def call_bedrock(prompt: str) -> str:
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

