# Pull official latest Python Docker image (Pulished with version 3.11.0)
FROM --platform=linux/amd64 python:3.11-slim-bullseye

# Set the working directory
WORKDIR /usr/auth

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE 8000

# Install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-openbsd gcc postgresql \
  && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# give permission to entrypoint.sh
RUN chmod +x /usr/auth/entrypoint.sh

# Execute entrypoint.sh
ENTRYPOINT ["/usr/auth/entrypoint.sh" ]

# Start up the backend server
CMD uvicorn src.main:auth_app --reload --workers 4 --host 0.0.0.0 --port 8000
