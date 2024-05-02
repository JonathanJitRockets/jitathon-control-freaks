# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /app

# Copy the clj-holmes executable and the entrypoint script into the container
COPY clj-holmes /app/clj-holmes
COPY entrypoint.sh /app/entrypoint.sh

# Install necessary packages
RUN apt-get update && apt-get install -y curl

# Make the executable and script runnable
RUN chmod +x /app/clj-holmes
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script as the entry point
ENTRYPOINT ["/app/entrypoint.sh"]