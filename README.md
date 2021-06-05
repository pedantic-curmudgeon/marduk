# marduk

## Table of Contents

1. [Scope](#scope-link)
1. [Folders](#folders-link)
1. [Files](#files-link)
1. [Local Execution](#local-execution-link)
1. [Fork Execution](#fork-execution-link)


<a id="scope-link"></a>
## 1. Scope
A basic repo with a custom `functions` module which includes examples
of CI/CD-related image build, publish, and test workflows using Docker,
Docker Compose, and GitHub Actions functionality.

When a pull request is opened, updated, or reopened to the `dev` branch:
1. A separate repository, [baldur](https://github.com/raegancbarker/baldur),
is cloned to obtain its `liquibase_changelog.sql` file which is used to
update the test database when the Docker Compose file is executed.
(If the branch in `marduk` from which the GitHub workflow was initiated
exists in `baldur`, that branch will be cloned from `baldur`. Otherwise,
the `dev` branch will be cloned.)
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
The results are also added to the pull request.

When a pull request is merged to the `dev` branch:
1. The `Dockerfile.test` image is built using the `dev` tag.
1. The image is published to Docker Hub.


<a id="folders-link"></a>
## 2. Folders

### [database](database)
SQLAlchemy database connection engines.

### [docker](docker)
Dockerfile, Docker Compose file, and local/server .env files.

### [functions](functions)
Custom module `marduk.functions`.

### [pytests](pytests)
Tests and test runner for `marduk.functions`.

### [.github/workflows](.github/workflows)
GitHub actions workflows.


<a id="files-link"></a>
## 3. Files

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
Environment variables used by the Docker Compose file for CI/CD server
executions.

### [pytests/test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [pytests/runner.py](pytests/runner.py)
Test runner to execute tests via `pytest`.

### [.github/workflows/on_pr_open_update_docker_build_test_.yml](.github/workflows/on_pr_open_update_docker_test.yml)
A custom workflow which performs the following actions on a pull request
open, update, or close to `dev`:
1. Checks out the `baldur` repo to get the `liquibase_changelog.sql` file
1. Checks out the `marduk` repo to get the Docker Compose tests file
1. Executes the `marduk` tests using the Docker Compose file
1. Uploads the `auto_tests.xml` test results as an artifact
1. Publishes the `auto_tests.xml` test results to the workflow

### [.github/workflows/on_pr_merge_docker_image_build_and_publish.yml](.github/workflows/on_pr_merge_docker_image_build_and_publish.yml)
A custom workflow which performs the following actions on a pull request
merge to `dev`:
1. Checks out the `marduk` repo
1. Builds the `Dockerfile.test` image with the `dev` tag
1. Publishes the image to Docker Hub

### [requirements.txt](requirements.txt)
Additional Python libraries required by `marduk`.


<a id="local-execution-link"></a>
## 4. Local Execution
To execute the tests locally:
1. Install [Docker](https://docs.docker.com/get-docker/) and
[Docker Compose](https://docs.docker.com/compose/install/).
1. Git clone `marduk` and `baldur` and check out the appropriate
branches.
1. Update `CHANGELOG_DIRECTORY` in `.env.test.local` in `marduk` to point
to the `baldur` directory.
1. Run the Docker Compose file from a terminal session in `/marduk/docker`.
    ```
    docker-compose -f docker-compose-test.yml --env-file .env.test.local up --build
    ```
1. The terminal will display logging information from all three of the
running containers.
1. Once the test executions have completed, press `Ctrl + C` in the terminal
to stop the Docker Compose stack.
1. Remove the Docker Compose stack, including the containers, network,
and volume, from a terminal session in `/marduk/docker`.
    ```
    docker-compose -f docker-compose-test.yml --env-file .env.test.local down --volumes
    ```


<a id="fork-execution-link"></a>

## 5. Fork Execution
To fork this repo and execute the CI/CD pipelines:
1. Create a fork of `marduk`.
1. Create a fork of `baldur`.
1. Navigate to `Settings > Secrets` in `marduk` and create the following
secrets:
    - `DOCKER_PASSWORD`: Docker Hub token.
    - `DOCKER_USERNAME`: Docker Hub user name.
    - `GH_TOKEN`: GitHub personal access token.
1. Navigate to `Settings > Branches` in `marduk` and add a new branch
protection rule.
    - Branch pattern name: `dev`
    - Require status checks to pass before merging: `✓`
    - Status checks that are required:
        - `Run Tests in Docker Compose`
        - `Unit Test Results`
    - Include Administrators: `✓`
1. In Docker Hub, create a repo named `marduk`.
1. Branch off of `dev` in both `marduk` and `baldur`, using the same name
for the new branch in both repos.
1. Make an update (such as adding a new text file) to the new branch
in `marduk`.
1. Open a pull request in `marduk` using `dev` as the base branch and
the new branch as the `head` branch.
1. The pull request will include a link to the to-be-completed GitHub
Actions workflow which was initiated by opening a pull request to the
`dev` branch.
1. Navigate to the `Checks` tab in the pull request or the `Actions` tab
in the `marduk` repo.
1. The `Test Docker Image With Docker Compose` workflow will now be running.
1. Once the workflow completes successfully, the pull request will be
eligible to be merged.
1. Merge the pull request.
1. Navigate to the `Checks` tab in the pull request or the `Actions` tab
in the `marduk` repo.
1. The `Build & Publish Docker Image` workflow will now be running.
1. Once the workflow completes successfully, refresh the `marduk`
repo in Docker Hub.
1. A new `marduk:dev` image will now be available.
