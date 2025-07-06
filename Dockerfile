# Ensure that the application is running through an official python build.
FROM python:3.10-slim

# Create and wrap the entire project around a directory "/app". All commands will run through this directory.
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Command to run your program
CMD ["python", "main.py"]