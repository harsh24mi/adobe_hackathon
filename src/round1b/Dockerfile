# src/round1b/Dockerfile

# Use a specific platform for compatibility.
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory.
WORKDIR /app

# Create directories for input and output data.
RUN mkdir -p /app/input /app/output

# Copy the requirements file for Round 1B.
COPY src/round1b/requirements.txt .

# --- THIS IS THE FINAL CORRECTION ---
# Use --extra-index-url to ADD the PyTorch CPU index, not replace the main one.
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy the pre-trained model you downloaded into the container.
COPY models/all-MiniLM-L6-v2 /app/models/all-MiniLM-L6-v2

# Copy the application code for Round 1B.
COPY src/round1b/analyze_docs.py .

# Command to run when the container starts.
CMD ["python", "analyze_docs.py"]