# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir -r requirements.txt && apt-get remove -y build-essential && apt-get clean

# Copy the rest of the application's code to the working directory
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
ENV SECRET_KEY="your_secret_key"

# Run app.py when the container launches
CMD ["python", "app.py"]
