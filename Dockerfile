FROM python:3.8-slim

# This needs to be passed in with docker run -e DISCORD_API_TOKEN=...
ENV DISCORD_API_TOKEN ''

WORKDIR app

# Update avalible packages
RUN apt-get update

# Install dependencies
RUN apt-get install ffmpeg python-dev gcc -y

# Copy everything we want over
COPY ./requirements.txt .
COPY ./src ./src

# Install python deps
RUN pip3 install -r ./requirements.txt

# Make executable
RUN chmod +x ./src/main.py

# The command that will run with `docker run ...`
CMD ["./src/main.py"]
