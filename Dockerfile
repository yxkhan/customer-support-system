#Dockerfile for a FastAPI application
# This Dockerfile sets up a FastAPI application using Uvicorn as the ASGI server
# Docker is a way of containerizing applications to run consistently across different environments (linux servers, local machines, etc.)
# It uses a slim version of Python 3.10 as the base image to keep the image size small
#Its like a virtual machine\environment but for the whole application
FROM python:3.10-slim

WORKDIR /app

COPY . .

# 👇 Debug: check all files inside the image
RUN ls -R /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
