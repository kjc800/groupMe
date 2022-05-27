GroupMe
===========
GroupMe is a web application that builds groups based on participants' skill levels. Groups can be created with all members being at the same skill level or created with a mentor/mentee objective.
Currently, GroupMe is tailored to work to create groups for class projects, however, the tool can be modified to fit any group activity.

## Technology
GroupMe is written in Python utilizing Flask to connect with the database and SQLAlchemy for querying. Data is stored within a CockroachDB cluster.

Start
==========
## Set up Database
1. Install CockroachDB.
2. Set up [cluster](https://www.cockroachlabs.com/docs/stable/start-a-local-cluster.html): cockroach start --insecure --listen-addr=localhost
3. Run the cluster: cockroach sql --insecure --host=localhost:26257
4. Create database and table.
Note: postgres will work fine as an alternate.

## Set up environment
1. Install pipenv: $ pip install pipenv
2. Enter pipenv shell: $ pipenv shell
3. Run the following installations:
- pipenv install flask
- pipenv install flask-sqlalchemy
- pipenv install psycopg2
- pipenv install psycopg2-binary
- pipenv install cockroachdb

## Run application locally
1. Enter pipenv shell
2. run app.py

Devpost: https://devpost.com/software/groupme