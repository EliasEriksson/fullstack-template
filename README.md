# lite-star
Playground for lite-star

## Setup
### Non python dependencies
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
### Virtual environment
Creates a python virtual environment and installs python dependencies 
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```
### Initialize the database
Database credentials can be given by either supplying environment variables or command line options. 

* Command line arguments
  ```bash
  ./main.py database create 
  ```
* Environment variables
  ```bash
  
  ```
If an option is omitted a default will be used in its place. 
Defaults:
* 
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
