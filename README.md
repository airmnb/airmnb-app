# airmnb-app

This is the home of Airmnb Api server.

## Setup Development Environment

### Prerequisites

Please make sure following prerequisites are all installed.

 - `python3`
 - `pip3`
 - `PostgreSQL server`, optional if you have a remote Airmnb database
 - `psql`
 - `virtualenv`, please follow the installation instructions in https://virtualenv.pypa.io/en/stable/installation/.

### Clone code repo and install dependencies

```
$ git clone https://github.com/airmnb/airmnb-app
$ cd airmnb-app
$ virtualenv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

### Setup Database

#### Create database

Plese use following command to create database
```
createdb airmmb
```

Reset database, in case of we change some schemas but hard to do auto migration.
```
db

# in postgres

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\q
```

#### Setup env vars

Create a `env` file in the directory root path and edit required env vars like `AMB_DATABASE_URI`.

```
export AMB_DATABASE_URI=postgresql://localhost/airmnb
```

After you have updated `env`, run below command to load env vars into the current environment:
```
source setenv.sh
```

Then you can verify it by running:
```
psql ${AMB_DATABASE_URI}
```
This should open psql and connect to the database you created. Then enter ```\q``` to quit.


#### Initialize database for database migration

If you just created database, it hasn't been initialized yet. Run following command:

```
python manage.py db downgrade base
```

This step is only needed for the first time after installation. It will create a table in public schema called 'alembic_version'. If 
you have run this before, then you shouldn't run this command again, otherwise the existing data will be wiped out.

#### Run database migration script

You may upgrade the db schema to the latest version by running:
```
python3 manage.py db upgrade head
```

### Add convenience commands

For your convenience, you can create an alias command in your .bash_profile to quickly jump to your working folder. For example, if you have cloned the repo to `~/airmnb-python-backend` and you want to use a shortcut `aa`, then you can add:

```
alias aa='cd ~/airmnb-app; . venv/bin/activate; . setenv.sh'
```

### Start server

After you have setup database, you can start the server by running:
```
start
```

### Test api

When server is running, you can test api by running:
```
curl localhost:5000/sys/health-check
```

This should return status code 200 and a text says 'OK'.

Or you can test api endpoint by running:
```
curl localhost:5000/api/1.0/users/
```

If users table is empty, you will get an empty list:
```
{
  "users": []
}
```

You can add a user into users table and try this api again, it should return the user you just created, for example:
```
echo "insert into users values ('e0a5d16c-3bed-11e8-b467-0ed5f89f718b', 'John', 'Smith', 'male', '1970-01-01', 'jsmith@company.com', 'unknown', NULL, now());" | psql ${AMB_DATABASE_URI}
```
Then you will get:
```
{
  "users": [
    {
      "avartar": null, 
      "createdAt": "2018-04-09T12:09:57.489351+00:00", 
      "dob": "1970-01-01", 
      "email": "jsmith@company.com", 
      "familyName": "John", 
      "gender": "male", 
      "givenName": "Smith", 
      "userId": "e0a5d16c-3bed-11e8-b467-0ed5f89f718b"
    }
  ]
}
```
