# Coffee Shop: Backend

Coffee shop app’s backend server hosted locally at `http://127.0.0.1:5000/`.

## Getting Started

### Installing Dependendies

The current project repo uses [`poetry`](https://python-poetry.org/docs/) to manage
dependencies among different Python packages, which is essential to reproducibility.
Following are steps for setting up and getting started:

First, ensure you are using the right version of Python (`^3.7`). You may want to
use [`pyenv`](https://github.com/pyenv/pyenv) to effectively manage multiple versions
of Python installation. You can then install `poetry`:
```
$ pip install poetry
```

Once you clone the current repo into your local machine, you can go inside the repo and run:
```
$ poetry install
```
to install the right versions of packages for running scripts in the project repo.

To use the new Python configuration that has been installed, you need to run:
```
$ poetry shell
```
which will activate the virtual environment for the project repo.

You can simply type:
```
$ exit
```
to exit from the virtual environment and return to the global (or system) Python installation.

### Setting up the Database

To create a new database, set:
```
$ export NEWDB=TRUE
```
which will make the server create a new database when it starts.

To make the created database persist, set:
```
$ export NEWDB=FALSE
```
which will stop the server from resetting the database when it starts.

### Running the Server

Finally, you can launch the backend server (within `src/` subdirectory):
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

For successful launch, make sure that the virtual environment has been activated.

### Testing

You can use [Postman](https://getpostman.com) to test the API endpoints.
The included Postman collection tests three user types:
1. **Customer**, who can only view basic drink info
2. **Barista**, who can also view detailed drink info
3. **Manager**, who can perform all actions including creation and deletion of drink items
