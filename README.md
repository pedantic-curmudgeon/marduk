# marduk

## Table of Contents

1. [Scope](#scope-link)
1. [Folders](#folders-link)
1. [Files](#files-link)


<a id="scope-link"></a>
## Scope
A basic repo with a custom `functions` module which includes examples
of CI/CD-related image build, publish, and test workflows using Docker,
Docker Compose, and GitHub Actions functionality.

When a push is made to the repo:
1. A separate repository, `baldur`, is cloned to obtain its
`liquibase_changelog.sql` file which is used to update the test database
when the Docker Compose file is executed. (If the branch in `marduk`
from which the GitHub workflow was initiated exists in `baldur`, that
branch will be cloned from `baldur`. Otherwise, the `dev` branch will be
cloned.)
1. A Docker Compose file builds the `marduk` image and starts it as a
container along with a standard
[MariaDB Docker image](https://hub.docker.com/_/mariadb) and a standard
[Liquibase Docker image](https://hub.docker.com/r/liquibase/liquibase).
1. On startup, the `Liquibase` container attempts to run `liquibase update`
on the `MariaDB` database container every 5 seconds until it succeeds.
1. On completion, the `Liquibase` container writes a success output
to the Docker volume defined in the Docker Compose file.
1. On startup, the `marduk` container checks the Docker volume every 5
seconds to see if `liquibase update` has been executed succesfully.
1. When `marduk` finds the `Liquibase` success output in the Docker
volume, it executes the test runner.
1. The test results are surfaced to the GitHub workflow as an artifact
on the workflow execution `Summary` and in the `Unit Test Results` job.

When a pull request is merged to the repo:
1. The `Dockerfile.test` image is built.
1. The image is published to Docker Hub.


<a id="folders-link"></a>
## Folders

### [database](database)
SQLAlchemy database connection engines.

### [docker](docker)
Dockerfile, Docker Compose file, and local/server .env files.

### [.github/workflows](.github/workflows)
GitHub actions workflows.

### [functions](functions)
Custom module `marduk.functions`.

### [pytests](pytests)
Tests and test runner for `marduk.functions`.


<a id="files-link"></a>
## Files

### [database/engines.py](database/engines.py)
Database engines with credentials to the test database used.

### [docker/Dockerfile.test](docker/Dockerfile.test)
A custom Docker image based on the standard Python 3.8.2 image. The repo
code is copied to the image, the `requirements.txt` is installed via
`pip`, and the `PYTHONPATH` is defined to include the parent folder of
the base repo code to allow `marduk` to be imported by Python.

### [docker/docker-compose-test.yml](docker/docker-compose-test.yml)
A custom Docker Compose file used to initialize a `MariaDB` database
container, `Liquibase` container,  and `marduk` test Dockerfile
container alongside a Docker volume and network to allow the containers
to interact and the tests to run.

### [docker/.env.test.local](docker/.env.test.local)
Environment variables used by the Docker Compose file for local executions.

### [docker/.env.test.server](docker/.env.test.server)
Environment variables used by the Docker Compose file for CI/CD server executions.

### [pytests/test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [pytests/runner.py](pytests/runner.py)
Test runner to execute tests via `pytest`.

### [.github/workflows/on_push_docker_build_test_.yml](.github/workflows/on_push_docker_test.yml)
A custom workflow which performs the following actions on any `push`:
1. Checks out the `baldur` repo to get the `liquibase_changelog.sql` file
1. Executes the tests using a Docker Compose file
1. Uploads the `auto_tests.xml` test results as an artifact
1. Publishes the `auto_tests.xml` test results to the workflow

### [.github/workflows/on_pr_merge_docker_image_build_and_publish.yml](.github/workflows/on_pr_merge_docker_image_build_and_publish.yml)
A custom workflow which performs the following actions on any pull request
`merge`:
1. Checks out the `marduk` repo
1. Builds the `Dockerfile.test` image
1. Publishes the image to Docker Hub

### [requirements.txt](requirements.txt)
Additional Python libraries required by `marduk`.
