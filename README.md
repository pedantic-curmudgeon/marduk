# marduk

## Scope
A basic repo with examples of CI/CD-related workflows using Docker,
DockerHub, and GitHub functionality. When a push is made to the repo:
1. A Dockerfile containing the repo code is built and the image is
published to DockerHub.
1. The tests are executed in a Docker container run from the newly-
published image.
1. The test results are surfaced to the GitHub workflow as an artifact
on the workflow execution `Summary` and in the `Unit Test Results` job.

## Folders

### [.github/workflows](.github/workflows)
Custom GitHub actions workflow.

### [functions](functions)
Custom module `marduk.functions`.

### [pytests](pytests)
Tests and test runner for `marduk.functions`.


## Files

### [Dockerfile](Dockerfile)
A custom Docker image based on the standard Python 3.8.2 image. The repo
code is copied to the image, the `requirements.txt` is installed via
`pip`, and the `PYTHONPATH` is defined to include the parent folder of
the base repo code to allow `marduk` to be imported by Python.

### [requirements.txt](requirements.txt)
Additional Python libraries required by `marduk`.

### [test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [runner.py](pytests/runner.py)
Test runner to execute tests via `pytest`.

### [on_push_docker_build_publish_and_test.yml](.github/workflows/on_push_docker_build_publish_and_test.yml)
A custom workflow which performs the following actions on any `push`:
1. Builds the `marduk` Dockerfile
1. Publishes the image to DockerHub
1. Executes the test runner in a Docker container
1. Uploads the `auto_tests.xml` test results as an artifact
1. Publishes the `auto_tests.xml` test results to the workflow

**Note**: Terminal commands are sent directly from the GitHub workflow
to the running Docker container as part of the actions performed within
the scope of the workflow.
