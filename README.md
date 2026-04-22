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

## Services and Tools

- Flask: Runs the web application and handles the recipe form, results page, rating route, and `/health` endpoint.
- pytest: Runs automated unit and integration tests.
- Bash scripts: Automate common Linux commands for installing, testing, smoke testing, and building the app.
- GitHub: Stores the project code and tracks changes with Git.
- GitHub Actions: Runs the CI/CD pipeline automatically when code is pushed or a pull request is opened.
- tar.gz artifact: Packages the web app into a compressed deployment file that can be downloaded from the pipeline.

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
4. Run tests.
5. Run the Flask smoke test.
6. Build the `.tar.gz` deployment artifact.
7. Upload the artifact in GitHub Actions.

This gives us proof that every push can be tested and packaged automatically.

## Developer Workflow

Create a branch for each feature:

```bash
git checkout main
git pull
git checkout -b feature-name
```

Before pushing, run the same checks that GitHub Actions will run:

```bash
bash scripts/test.sh
bash scripts/smoke_test.sh
bash scripts/build_artifact.sh
```

Then commit and push:

```bash
git add .
git commit -m "Describe the feature"
git push -u origin feature-name
```

After pushing, GitHub Actions runs automatically. If the run passes, open the Actions tab and download the `recipe-recommender-deployment` artifact.

## Useful Demo Commands

```bash
cd ~/Desktop/334-Dev-ops-Final
source .venv/bin/activate
bash scripts/test.sh
bash scripts/smoke_test.sh
bash scripts/build_artifact.sh
ls -lh dist/
```

## Team Members

- Michael Gifford
- Junyou Guo
