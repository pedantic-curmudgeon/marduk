# Start from Python 3.8.2 base image.
FROM python:3.8.2-alpine

# Set working directory.
WORKDIR /app/marduk

# Copy and install requirements file.
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy full repo code to image.
COPY . .

# Set Python path environment variable.
ENV PYTHONPATH "/app"

# Run Pytests.
CMD python3 /app/marduk/pytests/runner.py
