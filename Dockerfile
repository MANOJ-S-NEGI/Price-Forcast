# Use a Python 3.11 base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the entire application directory into the container
COPY . /code

# Expose port 7860
EXPOSE 7860

# Define the command to run your application (without Uvicorn)
CMD ["python", "app.py"]