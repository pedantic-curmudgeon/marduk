# marduk

## Scope
A basic repo with a custom `functions` module which includes examples
of CI/CD-related image build, publish, and test workflows using Docker,
DockerHub, Docker Compose, and GitHub Actions functionality.

When a push is made to the repo:
1. A Dockerfile containing the repo code is built and the image is
published to DockerHub.
1. A separate repository, `baldur`, is cloned to obtain its
`liquibase_changelog.sql` file which is used to update the test database
when the Docker Compose file is executed.
1. A Docker Compose file which uses the newly-published image with a
standard [MariaDB Docker image](https://hub.docker.com/_/mariadb) and
a standard [Liquibase Docker image](https://hub.docker.com/r/liquibase/liquibase)
is then run.
1. On startup, the `Liquibase` container attempts to run `liquibase update`
on the `MariaDB` database container every 5 seconds until it succeeds.
1. On completion, the `Liquibase` container writes a success output
to the Docker volume defined in the Docker Compose file.
1. On startup, the `marduk` container begins checking the Docker
volume every 5 seconds to see if `liquibase update` has been executed
succesfully.
1. When `marduk` finds the `Liquibase` success output in the Docker
volume, it executes the test runner.
1. The test results are surfaced to the GitHub workflow as an artifact
on the workflow execution `Summary` and in the `Unit Test Results` job.


## Folders

### [database](database)
SQLAlchemy database connection engines.

### [docker](docker)
Dockerfile, Docker Compose file, and .env.

### [.github/workflows](.github/workflows)
GitHub actions workflow.

### [functions](functions)
Custom module `marduk.functions`.

### [pytests](pytests)
Tests and test runner for `marduk.functions`.


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

### [docker/.env](docker/.env)
Environment variables used in the Docker Compose file.

### [pytests/test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [pytests/runner.py](pytests/runner.py)
Test runner to execute tests via `pytest`.

### [.github/workflows/on_push_docker_build_publish_and_test.yml](.github/workflows/on_push_docker_build_publish_and_test.yml)
A custom workflow which performs the following actions on any `push`:
1. Builds the `marduk` Dockerfile
1. Publishes the image to DockerHub
1. Checks out the `baldur` repo to get the `liquibase_changelog.sql` file
1. Executes the tests using a Docker Compose file
1. Uploads the `auto_tests.xml` test results as an artifact
1. Publishes the `auto_tests.xml` test results to the workflow

### [requirements.txt](requirements.txt)
Additional Python libraries required by `marduk`.
