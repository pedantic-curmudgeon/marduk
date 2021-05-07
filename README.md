# marduk

## Scope
A basic repo with examples of various CI/CD-related workflows using a
combination of Docker, DockerHub, and GitHub functionality.


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
`pip` and the `$PYTHONPATH` is defined to include the parent folder of
the base repo code to allow `marduk` to be imported by Python.

### [requirements.txt](requirements.txt)
Additional Python libraries required by `marduk`.

### [test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [runner.py](pytests/runner.py)
Test runner to execute tests via `pytest`.

### [docker_image_build_push_workflow.yml](.github/workflows/docker_image_build_push_workflow.yml)
A custom workflow which performs the following actions on any `push`:
1. Builds the `marduk` Dockerfile
1. Publishes it to DockerHub
1. Executes the test runner
1. Uploads the `auto_tests.xml` test results as an artifact
1. Publishes the `auto_tests.xml` test results to the workflow.
