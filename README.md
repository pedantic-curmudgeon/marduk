[![Automated Tests](https://github.com/raegancbarker/marduk/actions/workflows/on_pr_open_update_docker_test.yml/badge.svg)](https://github.com/raegancbarker/marduk/actions/workflows/on_pr_open_update_docker_test.yml)

# marduk

## Table of Contents

1. [Scope](#scope-link)
1. [Folders](#folders-link)
1. [Files](#files-link)
1. [Local Execution](#local-execution-link)
1. [Template Execution](#fork-execution-link)
1. [Troubleshooting](#troubleshooting-link)


<a id="scope-link"></a>
## 1. Scope
A basic repo with a custom `functions` module which includes examples
of CI/CD-related image test and build and publish workflows using Docker,
Docker Compose, and GitHub Actions functionality.

When a pull request is opened, updated, or reopened to the `dev` branch:
1. A separate repository, [baldur](https://github.com/raegancbarker/baldur),
is cloned to obtain its `liquibase_changelog.sql` file which is used to
update the test database when the Docker Compose file is executed.
The branch cloned from `baldur` will match the `head` branch of the PR
initiated in `marduk`.
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
on the workflow execution `Summary` and in the `Test Results` job.
The results are also added as a comment on the pull request.
1. The code coverage results are added as a comment on the pull request.


When a pull request is merged to the `dev` branch:
1. The `Dockerfile.test` image is built using the `dev` tag.
1. The image is published to Docker Hub.


<a id="folders-link"></a>
## 2. Folders

### [database](database)
SQLAlchemy database connection engines.

### [docker](docker)
Dockerfile, Docker Compose file, and .env file.

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

### [docker/.env.test](docker/.env.test)
Environment variables and build arguments used by the Dockerfile and
the Docker Compose file.

### [pytests/test_functions.py](pytests/test_functions.py)
Test class with test scenarios for the `marduk.functions` module.

### [pytests/runner.py](pytests/runner.py)
Test runner to execute tests via `pytest` with code coverage
analysis via `pytest-cov`.

### [.github/workflows/on_pr_open_update_docker_build_test_.yml](.github/workflows/on_pr_open_update_docker_test.yml)
A custom workflow which performs the following actions on a pull request
open, update, or close to `dev`:
1. Checks out the `marduk` repo to get the Docker Compose test files
1. Checks out the `baldur` repo to get the `liquibase_changelog.sql` file
1. Executes the `marduk` tests and coverage analysis using the Docker
Compose file
3. Uploads the `auto_tests.xml` test results as a workflow artifact
4. Uploads the `coverage.xml` and `htmlcov` coverage results as a workflow
artifact
1. Publishes the `auto_tests.xml` test results to a workflow job and a
PR comment
1. Publishes a summary of the coverage results as a PR comment

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
1. Git clone `marduk` and `baldur` to the same parent directory and
check out the appropriate branches.
1. Set the `ENV_VAR` environment variable and run the Docker Compose
file from a terminal session in `/marduk/docker`.
    ```
    $ ENV_VAR="abc123def456"
    $ export ENV_VAR
    $ docker-compose -f docker-compose-test.yml --env-file .env.test up --build
    ```
1. The terminal will display logging information from all three of the
running containers.
    ```
    Successfully tagged test/marduk:latest
    Creating db_container ... done
    Creating liquibase_container ... done
    Creating repo_container      ... done
    Attaching to db_container, liquibase_container, repo_container
    ```
1. Once the test executions have completed as shown below, press
`Ctrl + C` in the terminal to stop the Docker Compose stack.
    ```
    liquibase_container | Liquibase: Update has been successful.
    liquibase_container exited with code 0
    repo_container | ============================= test session starts ==============================
    repo_container | platform linux -- Python 3.8.2, pytest-6.2.3, py-1.10.0, pluggy-0.13.1 -- /usr/local/bin/python3
    repo_container | cachedir: .pytest_cache
    repo_container | rootdir: /app/marduk
    repo_container | plugins: cov-2.12.1
    repo_container | collecting ... collected 6 items
    repo_container |
    repo_container | pytests/test_functions.py::TestFunctions::test_stringify_list_001 PASSED [ 16%]
    repo_container | pytests/test_functions.py::TestFunctions::test_stringify_list_002 PASSED [ 33%]
    repo_container | pytests/test_functions.py::TestFunctions::test_db_alive_001 PASSED       [ 50%]
    repo_container | pytests/test_functions.py::TestFunctions::test_db_alive_002 PASSED       [ 66%]
    repo_container | pytests/test_functions.py::TestFunctions::test_query_db_001 PASSED       [ 83%]
    repo_container | pytests/test_functions.py::TestFunctions::test_environment_variable_001 PASSED [100%]
    repo_container |
    repo_container | ---------------- generated xml file: /app/marduk/auto_tests.xml ----------------
    repo_container |
    repo_container | ----------- coverage: platform linux, python 3.8.2-final-0 -----------
    repo_container | Name                     Stmts   Miss Branch BrPart  Cover
    repo_container | ----------------------------------------------------------
    repo_container | __init__.py                  2      0      0      0   100%
    repo_container | database/__init__.py         1      0      0      0   100%
    repo_container | database/engines.py         15      0      0      0   100%
    repo_container | functions/__init__.py        1      0      0      0   100%
    repo_container | functions/functions.py      20      0      8      0   100%
    repo_container | ----------------------------------------------------------
    repo_container | TOTAL                       39      0      8      0   100%
    repo_container | Coverage HTML written to dir htmlcov
    repo_container | Coverage XML written to file coverage.xml
    repo_container |
    repo_container | ============================== 6 passed in 2.53s ===============================
    repo_container exited with code 0
    ```
1. *(Optional)* Copy the test and coverage results from the Docker
container to the local machine.
    ```
    docker cp repo_container:/app/marduk/coverage.xml .
    docker cp repo_container:/app/marduk/htmlcov ./htmlcov
    ```
1. Remove the Docker Compose stack, including the containers, network,
and volume, from a terminal session in `/marduk/docker`.
    ```
    $ docker-compose -f docker-compose-test.yml --env-file .env.test down --volumes
    ```
1. After executing locally more than once, dangling Docker images can
begin to accumulate. Use the following to remove orphaned images:
    ```
    $ docker image prune
    ```


<a id="fork-execution-link"></a>

## 5. Template Execution
To create a new repo from this template and execute the CI/CD pipelines:
1. Create a repo from the `marduk` template.
1. Create a repo from the `baldur` template.
1. Navigate to `Settings > Secrets` in `marduk` and create the following
secrets:
    - `DOCKER_PASSWORD`: Docker Hub token.
    - `DOCKER_USERNAME`: Docker Hub username.
    - `GH_TOKEN`: GitHub personal access token.
    - `ENV_VAR`: abc123def456
1. In Docker Hub, create a repo named `marduk`.
1. In GitHub, branch off of `dev` in `marduk`.
1. Make an update (such as adding a new text file) to the new branch
in `marduk`.
1. Open a pull request in `marduk` using `dev` as the base branch and
the new branch as the `head` branch.
1. The pull request will refresh to include links to the to-be-completed
GitHub Actions workflows which were initiated by opening a pull request
to the `dev` branch.
1. Navigate to the `Checks` tab in the pull request or the `Actions` tab
in the `marduk` repo.
1. The `Automated Tests` workflow will now be running.
1. Once the workflow completes successfully, merge the pull request.
1. Navigate back to the `Checks` tab in the pull request or the
`Actions` tab in the `marduk` repo.
1. The `Docker Image Build & Publication` workflow will now be running.
1. Once the workflow completes successfully, refresh the `marduk`
repo in Docker Hub.
1. A new `marduk:dev` image will now be available.
1. To enable branch protections, navigate to `Settings > Branches` in
`marduk` and add a new branch protection rule.
    - Branch pattern name: `dev`
    - Require status checks to pass before merging: `✓`
    - Status checks that are required:
        - `Docker Compose Tests`
        - `Test Results`
    - Include Administrators: `✓`
    - Note: This step must be completed after the actions have run once.


<a id="troubleshooting-link"></a>
## 6. Troubleshooting

### Local Execution
If `repo_container` begins running tests before `liquibase_container`
has exited with a `0` exit code:
1. Stop `Docker Compose` with `Ctrl + C`.
1. Run the `docker-compose` down command.
    ```
    $ docker-compose -f docker-compose-test.yml --env-file .env.test down --volumes
    ```
1. The following should be logged in the terminal.
    ```
    Removing repo_container      ... done
    Removing liquibase_container ... done
    Removing db_container        ... done
    Removing network docker_default
    Removing volume compose_volume
    ```
1. If `Removing volume compose_volume` does not show in the
terminal, check if the volume `compose_volume` still exists.
    ```
    $ docker volume ls
    ```
1. If the volume exists, remove it.
    ```
    $ docker volume rm compose_volume
    ```
1. Attempt to re-run the local tests.

### Template Execution
If the `Test Results` check does not appear after `Docker Compose Tests`
completes without errors:
1. Merge the open PR into `dev`.
1. Make a new change to the feature branch.
1. Create a new PR into `dev`.
1. Confirm the test actions execute and the `Test Results` check now
appears.
1. Repeat if necessary.
