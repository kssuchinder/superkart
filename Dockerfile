# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run the Flask application
# Assuming your Flask app is in a file named 'app.py' and the app instance is called 'app'
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860", "--without-threads"]
