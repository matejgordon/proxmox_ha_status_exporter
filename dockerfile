FROM python:3.8-alpine

RUN apk update && apk add python3-dev build-base

# Create a virtual environment
RUN python3 -m venv /opt/venv
# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the source code and requirements file
COPY ./src/ ./requirements.txt ./


# Install requirements in the virtual environment
RUN pip3 install -r requirements.txt

# Expose the port
EXPOSE 9562

# Run the application
CMD [ "python", "ha_resource_status_exporter.py" ]