# src/round1a/Dockerfile

# Use a specific platform for compatibility as requested[cite: 23, 24].
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Create directories for input and output data as specified in the execution plan[cite: 25].
RUN mkdir -p /app/input /app/output

# Copy the requirements file first to leverage Docker's layer caching.
COPY src/round1a/requirements.txt .

# Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script into the container's working directory.
COPY src/round1a/extract_outline.py .

# This is the command that will run when the container starts.
# It executes your Python script to process the PDFs.
CMD ["python", "extract_outline.py"]