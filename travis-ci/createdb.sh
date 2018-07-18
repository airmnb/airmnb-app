#!/bin/bash

DB_NAME=airmnb

createdb -U postgres ${DB_NAME}
psql -c "create schema q" ${DB_NAME}
