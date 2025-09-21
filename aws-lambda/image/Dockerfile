# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy cert into the image (inside Lambda task root)
COPY cert/aws.pem ${LAMBDA_TASK_ROOT}/cert/aws.pem

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy .env
COPY .env ${LAMBDA_TASK_ROOT}/.env

RUN chmod 644 ${LAMBDA_TASK_ROOT}/cert/aws.pem ${LAMBDA_TASK_ROOT}/.env

# Set Lambda handler
CMD ["app.lambda_handler"]
