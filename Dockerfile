# Ensure that the application is running through an official python build.
FROM python:3.10-slim

# Install Tkinter system dependencies (must come before pip install)
RUN apt-get update && apt-get install -y python3-tk && rm -rf /var/lib/apt/lists/*

# Create and wrap the entire project around a directory "/app". All commands will run through this directory.
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Command to run your program
CMD ["python", "main.py"]
