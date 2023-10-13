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
* `apt install python3.x-dev`\
  `x` is your python 3 minor version
* `apt install build-essential cargo`
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
python -m pip install -r requirements.txt
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
### Generate secrets
It is possible to skip this step for development. By default, the configuration will load default public/private keys
and set the password pepper to an empty string this key guarantees consistency but is also COMPLETELY UNSECURE. 
When running in production mode setting these secrets is required. 

#### JWT public / private keys
Use `openssl` to generate private and public key used for signing and verifying JWTs:
```bash
openssl genrsa -out jwt_private_key.pem 4196
openssl rsa -in jwt_private_key.pem -pubout -out jwt_public_key.pub
```
Export keys contents to environment variables:
```bash
export JWT_PRIVATE_KEY=$(echo $(cat jwt_private_key.pem))
export JWT_PUBLIC_KEY=$(echo $(cat jwt_public_key.pub))
```
#### Password pepper
This could set and generated with:
```bash
export PASSWORD_PEPPER=$(python -c "import secrets;print(secrets.token_hex(64))")
```
If no pepper is preferred set its value to an empty string.


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
- [x] lite-start hello world
- [x] database abstraction
- [x] user CRUD
- [x] storing passwords
- [x] authentication
- [x] issue JWTs
- [x] `GET /auth`
- [ ] test `GET /auth`
- [ ] logging
- [ ] use pypy?
    * use h11 over httptools?
    * other packages might need to change to be compatible
- [ ] email verification?
