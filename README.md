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
* [alembic](https://pypi.org/project/alembic/)

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
If neither a command line argument nor an environment variable is present for a value a default will be used.
* Command line arguments using default values
  ```bash
  ./main.py database migrate --username lite-star --password lite-star --database lite-star --host localhost --port 5432
  ```
* Environment variables using default values
  ```bash
  export POSTGRES_USERNAME=lite-star POSTGRES_PASSWORD=lite-star POSTGRES_DATABASE=lite-star POSTGRES_HOST=localhost POSTGRES_PORT=5432 && ./main.py database migrate
  ```
## Migrating the database
Alembic is used for database migrations. This projects commandline interface wraps around the alembic CLI
to apply some opinionated options and minor automation. This CLI also injects the sqlalchemy database url into
alembic. This means that alembic does not have a database url configured and will not work if called manually without
extra configuration. 
Always prefer to use this projects CLI over alembics. If support for something from alembic is missing in this CLi
try to implement support for it rather than calling alembic manually.
1. Create a new alembic revision.
   ```bash
   python main.py database revision -m "This is an optional message"
   ```
2. make sure that the revision created in `./migrations/versions` is correct.
3. Apply the revision
   ```bash
   python main.py database migrate
   ```

## TODO
- [x] implement postgres
  - [x] change uuid id to server default 
  - [x] setup database tests to be able to use postgres
    * dynamic connection string
  - [x] setup CI to be able to use postgres 
    * [more reading...](https://medium.com/qest/database-for-ci-cd-tests-quickly-and-inexpensively-96e3116ce72f)
    * [even more reading...](https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers)
- [x] install and setup [alembic](https://alembic.sqlalchemy.org/en/latest/)
  - [x] call alembic from cli script
    - alembic internal commands api [docs](https://alembic.sqlalchemy.org/en/latest/api/commands.html)
    - some [SO thread](https://stackoverflow.com/questions/24622170/using-alembic-api-from-inside-application-code)
- [ ] database abstraction
- [ ] lite-start hello world
- [ ] logging
- [ ] storing passwords
- [ ] authentication
- [ ] issue JWTs
- [ ] `GET /auth`
- [ ] test `GET /auth`
- [ ] email verification?
