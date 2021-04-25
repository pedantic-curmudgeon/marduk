# Start from Python 3.8.2 base image.
FROM python:3.8.2-alpine

# Set working directory.
# Must be within the Python path.
# import os
# print(os.path)
WORKDIR /usr/local/lib/python3.8/site-packages/marduk

# Copy requirements file.
COPY requirements.txt requirements.txt

# Install requirements file.
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy full repo code to image.
COPY . .

# Run tests w/o CMD.
# RUN python3 pytests/test_functions.py
# RUN python3 pytests/runner.py

# Only 1 CMD instruction permitted per Dockerfile.
CMD [ "python3", "pytests/runner.py" ]


# To Build:
# docker build --tag marduk_tests .

# To View Images:
# docker images

# To Remove:
# docker image rm <IMAGE ID>

# To View Volumes:
# docker volume ls

# To View Volume Details:
# docker volume inspect <VOLUME NAME>

# To Run:
# docker run marduk_tests
# docker run marduk_tests

# Need to figure out the rest as well. Naming, etc.
# docker run marduk_tests -d --name=god_of_babylon -v marduk_volume:/app/repo/pytests
