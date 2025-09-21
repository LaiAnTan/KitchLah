# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set Lambda handler
CMD ["app.lambda_handler"]
