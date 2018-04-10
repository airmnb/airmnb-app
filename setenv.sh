#!/bin/bash

export DATABASE_URI=postgres://qstqzkzu:wIRQ-yASKMaE7hEdABZCD7cSKUuC40DA@stampy.db.elephantsql.com:5432/qstqzkzu

echo Database: $DATABASE_URI

# load aliases for convenience
FILE_DIR=$(dirname "${BASH_SOURCE}")
ALIASES="${FILE_DIR}/.aliases"
if [ -e "$ALIASES" ]; then
	source "$ALIASES"
fi
PYTHONSTARTUP_FILE="${FILE_DIR}/.pythonstartup"
if [ -e "${PYTHONSTARTUP_FILE}" ]; then
	export PYTHONSTARTUP="${PYTHONSTARTUP_FILE}"
fi
