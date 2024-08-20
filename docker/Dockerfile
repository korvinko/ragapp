# Use an official Python runtime as a parent image
FROM python:3.12.5

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./ /app/

## Install any needed packages specified in requirements.txt
## Ensure that all dependencies are installed
RUN pip install --no-cache-dir -r requirements.txt

## Install uvicorn
RUN pip install --no-cache-dir uvicorn

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "4_rest_app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]