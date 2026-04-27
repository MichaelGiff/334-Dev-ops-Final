# Recipe Recommender Web App

Simple Flask web app for a Linux DevOps / CI/CD final project. The app lets a user enter meal type, ingredients, and dietary preference, then returns matching recipe recommendations from a local recipe list.

The main focus of this project is the automation pipeline: install, test, smoke test, build, and package the web app as a `.tar.gz` artifact.

## Tech Stack

- Python
- Flask
- HTML, CSS, and basic JavaScript
- pytest
- Bash scripts for Linux automation
- GitHub Actions for CI/CD

## Project Structure

```text
app.py                  Flask web app and routes
recommender.py          Recipe matching and rating logic
recipes.py              Local recipe data
templates/index.html    Main web page
static/style.css        Minimal styling
tests/                  Unit and integration tests
scripts/                Linux automation scripts
.github/workflows/      GitHub Actions pipeline
```

## Install Locally

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
bash scripts/install.sh
```

The install script upgrades `pip` and installs everything from `requirements.txt`.

## Run the Web App

```bash
source .venv/bin/activate
flask --app app run
```

Then open:

```text
http://127.0.0.1:5000
```

Health check endpoint:

```text
http://127.0.0.1:5000/health
```

## Run Tests

```bash
bash scripts/test.sh
```

This runs:

- Python syntax/build check with `compileall`
- Unit tests for recommender logic
- Flask integration tests for app routes

## Run a Smoke Test

```bash
bash scripts/smoke_test.sh
```

This starts the Flask app on port `5050` and checks:

```text
http://127.0.0.1:5050/health
```

This proves the app can boot and respond like a real service.

## Build the Deployment Artifact

```bash
bash scripts/build_artifact.sh
```

This creates:

```text
dist/recipe-recommender-<commit>.tar.gz
```

The `.tar.gz` file is the deployable app artifact for the project.

## GitHub Actions Pipeline

The CI/CD pipeline should automatically:

1. Check out the repository.
2. Set up Python on Ubuntu Linux.
3. Install dependencies.
4. Run the linter.
5. Run tests.
6. Run the Flask smoke test.
7. Build the `.tar.gz` deployment artifact.
8. Upload the artifact in GitHub Actions.

This gives us proof that every push can be tested and packaged automatically.

## Clean Demo Commands

Create a tiny change on a feature branch:

```bash
git checkout -b demo-small-change
```

Run the same validation locally that GitHub Actions will run:

```bash
cd ~/Desktop/334-Dev-ops-Final
source .venv/bin/activate
bash scripts/install.sh
bash scripts/test.sh
bash scripts/smoke_test.sh
bash scripts/build_artifact.sh
ls -lh dist/
```

Commit and push:

```bash
git add .
git commit -m "Add small demo change"
git push -u origin demo-small-change
```

Then open GitHub and show:

1. The pull request or branch push.
2. The Actions tab.
3. The green workflow run.
4. The `recipe-recommender-deployment` artifact.

## Simple Class Explanation

- We write code on a branch instead of directly on `main`.
- We push the branch to GitHub.
- GitHub Actions starts automatically.
- The pipeline creates a clean Linux environment.
- It installs dependencies.
- It lints the code.
- It runs automated tests.
- It starts the Flask app and checks the health endpoint.
- It builds a `.tar.gz` deployment artifact.
- It uploads the artifact so the build result can be downloaded.
- making small change for the demo

## Team Members

- Michael Gifford
- Junyou Guo
