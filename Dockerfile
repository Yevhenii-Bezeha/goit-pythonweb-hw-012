FROM python:3.11

WORKDIR /app

# Install system dependencies for Sphinx
RUN apt-get update && apt-get install -y \
    make \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build documentation
RUN cd docs && make html

# Expose ports for both API and documentation
EXPOSE 8000 8080

# Create a script to run both API and documentation server
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]