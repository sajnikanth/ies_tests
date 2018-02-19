FROM python:2.7

# Set a working directory
WORKDIR /ies_tests

# Copy the current directory contents into the container at the working dir
ADD . /ies_tests

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run tests when the container launches
CMD ["python", "run.py"]
