# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


RUN pip install --no-cache-dir -r requirements.txt  

WORKDIR /app/flask_app

EXPOSE 5000 9999
# Run the Python script when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
