# CS50 CI Action

A GitHub Action / CI workflow for validating CS50 problem-set tests by running them against known solutions.
It helps instructors verify that changes to their tests don’t accidentally break correct solutions or fail to catch incorrect ones.

## Goal

- ensure that valid (student) solutions continue to pass after test updates
- confirm that intentionally invalid solutions fail
- automation as part of a CI workflow (e.g. in Pull Requests)

## Features

- clones both problems and solutions repositories (solutions repo may be private)
- authenticates via a GitHub App
- iterates through all provided solutions and runs them against respective problem tests
- reports pass/fail results in console output and/or
- posts results back into PR comments (if run as action triggered by a Pull Request)
- supports running locally (Python or Docker)

## Quickstart

### Prerequisites 

- a ```.env``` file (or environment variables) specifying required config (see ```.env.sample```)
- a GitHub App with access to clone both repositories and comment on pull requests
- Python or Docker

#### Running locally

```python src/main.py```

#### Running via Docker

```docker compose up --build```

#### Example GitHub Actions Setup


Below you can find GitHub Action which will run on Pull Requests:

```
name: CS50 CI

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  run-cs50-ci:
    name: Run CS50 Continuous Integration
    runs-on: ubuntu-latest

    steps:
      - name: Run CS50 CI Action
        uses: LeoKle/cs50-ci-action@main
        with:
          app-id: ${{ secrets.GH_APP_ID }}
          install-id: ${{ secrets.GH_INSTALL_ID }}
          private-key: ${{ secrets.GH_TOKEN_B64 }}
          problems-repository: ${{ github.repository }}
          problems-branch: ${{ github.event.pull_request.base.ref }}
          solutions-repository: HSDDigitalLabor/solutions
          solutions-branch: main
```

## Configuration

| Variable             | Description                                          |
| -------------------- | ---------------------------------------------------- |
| `APP_ID`             | GitHub App ID                                        |
| `INSTALL_ID`         | GitHub App install ID                                |
| `PRIVATE_KEY_B64`    | GitHub App private key (in B64)                      |
| `PROBLEMS_REPO`      | GitHub `owner/repo` for problem definitions          |
| `PROBLEMS_BRANCH`    | the branch of the problem repo that should be used   |
| `SOLUTIONS_REPO`     | GitHub `owner/repo` for solutions                    |
| `SOLUTIONS_BRANCH`   | the branch of the solutions repo that should be used |