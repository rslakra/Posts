#FROM public.ecr.aws/docker/library/python:3.12.7-slim
#Specifies the Python base image.
FROM python:3.12-slim

# Arguments
ARG APP_ENV=develop
ARG API_ENV=develop

# Define Env Variables
ENV APP_ENV=$APP_ENV
ENV API_ENV=$API_ENV
ENV APP_NAME=posts-iws
# The port the server is listening on (override with 'docker run -e PORT=...').
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Sets the working directory inside the Docker container at `/app`
WORKDIR /app

# Installs the Python dependencies specified in the `requirements.txt` file (a separate layer, so it is cached until
# the requirements change).
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copies the current directory (.) from the host machine to the `/app` directory in the Docker container.
COPY . /app

# EXPOSE is for documentation only - does not do anything
EXPOSE 8080

# Run the FastAPI app with uvicorn. The shell form is used, so ${PORT} is expanded and 'exec' makes uvicorn PID 1
# (it receives the stop signals of 'docker stop').
# For development with auto-reload: uvicorn main:app --host 0.0.0.0 --port 8080 --reload
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
