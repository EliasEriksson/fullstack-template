# lite-star
Playground for lite-star

## Dependencies
### Non Python dependencies
* [postgresql](https://www.postgresql.org/)
### Python dependencies (excluding peer dependencies):
* [click](https://pypi.org/project/click/)
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
* [pytest](https://pypi.org/project/pytest/)
* [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)
* [psycopg](https://pypi.org/project/psycopg/)
* [black](https://pypi.org/project/black/)

## Setup
### Install non python dependencies
* [postgresql](https://www.postgresql.org/download/)
### Configure postgres user
create the lite-star user and database
```sql
CREATE DATABASE "lite-star";
CREATE DATABASE "lite-star-test";
-- OBS! Do not use this password for anything other than local development!
CREATE USER "lite-star" WITH ENCRYPTED PASSWORD 'lite-star';
GRANT ALL PRIVILEGES ON DATABASE "lite-star" to "lite-star";
GRANT ALL PRIVILEGES ON DATABASE "lite-star-test" to "lite-star";
```

### Installing python dependencies in virtual environment
Create a python virtual environment and install python dependencies 
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements_dev.txt
```

### Initialize the database
Database credentials can be given by either supplying environment variables or command line arguments. 
If neither an argument nor an environment variable is present for a value a default will be used.
* Command line arguments using default values
  ```bash
  ./main.py database create --username lite-star --password lite-star --database lite-star --host localhost --port 5432
  ```
* Environment variables using default values
  ```bash
  export POSTGRES_USERNAME=lite-star POSTGRES_PASSWORD=lite-star POSTGRES_DATABASE=lite-star POSTGRES_HOST=localhost POSTGRES_PORT=5432 && ./main.py
  ```
  
## TODO
- [ ] install and setup [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [ ] call alembic from cli script [SO thread](https://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code)
- [ ] implement postgres
  - [ ] change uuid id to server default 
  - [x] setup database tests to be able to use postgres
    * dynamic connection string
  - [x] setup CI to be able to use postgres 
    * [more reading...](https://medium.com/qest/database-for-ci-cd-tests-quickly-and-inexpensively-96e3116ce72f)
    * [even more reading...](https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers)
- [ ] database abstraction
- [ ] lite-start hello world
- [ ] logging
- [ ] storing passwords
- [ ] authentication
- [ ] issue JWTs
- [ ] `GET /auth`
- [ ] test `GET /auth`
- [ ] email verification?
