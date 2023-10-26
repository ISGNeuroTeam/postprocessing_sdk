# Use an official Python runtime as a parent image
FROM python:3.9.7

# Describe credits
#LABEL authors="Enter yout name here"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install --extra-index-url http://s.dev.isgneuro.com/repository/ot.platform/simple --trusted-host s.dev.isgneuro.com postprocessing-sdk

# Copy source code
COPY . /app
