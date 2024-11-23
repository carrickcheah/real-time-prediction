# start with python 3.10 slim image
FROM python:3.10-slim

# set the working directory in the container    
WORKDIR /app

# Install Python Poetry with version 1.8.4
RUN pip install poetry==1.8.4

# Copy the source code to the working directory
COPY . /app

# Install the dependencies
RUN poetry install


# Run the application
CMD ["poetry", "run", "python", "src/main.py"]



# # copy the dependencies file to the working directory
# COPY requirements.txt .

# # install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # copy the content of the local src directory to the working directory
# COPY . .

# # command to run on container start
# CMD [ "python", "./ingest.py" ]

