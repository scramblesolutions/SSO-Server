# Dockerfile

FROM python:3.10-alpine

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    mariadb-connector-c-dev \
    mariadb-dev \
    pkgconfig

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install them
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Set the working directory
WORKDIR /app

# Copy the entrypoint script and set the entrypoint
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
