# Start from Python 3.8.2 base image.
FROM python:3.8.2-alpine

# Set working directory to Python path.
# python
# import os
# print(os.path)
# WORKDIR /usr/local/lib/python3.8/site-packages/marduk

WORKDIR /app/marduk

# Copy and install requirements file.
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy full repo code to image.
COPY . .

# Run tests w/o CMD.
# RUN python3 pytests/test_functions.py
# RUN python3 pytests/runner.py

# Only 1 CMD instruction permitted per Dockerfile.
# Does this move outside of the Dockerfile?
# How do we surface the results from the tests?

# NEXT: Does this all make sense?
# So, to break it down:
# 1. Dockerfile: Copies code into path; installs requirements.
# 2. workflow.yaml: Specifies container-image to use; issues "run:" commands;
# publishes artifacts (for test results!).

# Do we just need a placeholder entry point? Or none at all? Below command is removed?

ENV PYTHONPATH "${PYTHONPATH}:/app"

# Relative path works!
# CMD python3 pytests/runner.py (Relative path works.)

# Absolute path works!
# CMD python3 /app/marduk/pytests/runner.py

# Absolute path with WORKDIR reference works!
CMD python3 "${WORKDIR}/pytests/runner.py

# CMD [ "python3", "pytests/runner.py" ]



# I think this might be a good idea:
# https://linuxhit.com/how-to-create-docker-images-with-github-actions/
# https://www.petefreitag.com/item/903.cfm
# https://stackoverflow.com/questions/56726429/how-to-run-multiple-commands-in-one-github-actions-docker
# https://github.com/marketplace/actions/docker-run-action
# https://stackoverflow.com/questions/63472909/github-actions-run-steps-in-container



# Then we issue separate commands in the docker-image.yml?
# First we build the image.
# Then we publish the image.
# Then we run the image as a container.
# Then we execute the tests.
# Then we publish the test artifacts?
# Done?


# To Build:
# docker build --tag marduk_tests .

# To View Images:
# docker images

# To Remove Image:
# docker image rm <IMAGE ID>

# To View Volumes:
# docker volume ls

# To View Volume Details:
# docker volume inspect <VOLUME NAME>

# To Run:
# docker run --name god_of_babylon marduk_tests
# docker run -d --name god_of_babylon marduk_tests

# Need to figure out the rest as well. Naming, etc.
# -v marduk_volume:/app/repo/pytests


# TODO: Run the container with a name, in the background(?), and with a volume (for the XML)?
