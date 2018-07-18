#!/bin/bash

DB_NAME=airmnb

createdb -U postgres ${DB_NAME}
psql -c 'create extension "uuid-ossp";' ${DB_NAME}
