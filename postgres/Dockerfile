# Use the official PostgreSQL image as the base image
FROM postgres:14.1-alpine

# Install build dependencies and pgvector
RUN apk add --no-cache \
      postgresql-dev \
      gcc \
      musl-dev \
      make \
      git \
    && git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install \
    && apk del gcc musl-dev make git \
    && rm -rf /pgvector

# Copy any custom configuration or initialization scripts if needed
# COPY ./your-custom-config /docker-entrypoint-initdb.d/
