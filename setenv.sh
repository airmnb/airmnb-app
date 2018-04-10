#!/bin/bash

export DATABASE_URI=postgres://qstqzkzu:wIRQ-yASKMaE7hEdABZCD7cSKUuC40DA@stampy.db.elephantsql.com:5432/qstqzkzu
export WECHAT_APP_ID=wxb945640b6fd4a85b
export WECHAT_APP_SECRET=

FILE_DIR=$(dirname "${BASH_SOURCE}")

# load development environment
LOCAL_ENV="${FILE_DIR}/env"
if [ -e "${LOCAL_ENV}" ]; then
	source "${LOCAL_ENV}"
fi

echo -e "\033[1;32mDATABASE_URI: \033[0;36m${DATABASE_URI}\033[0m"

# load aliases for convenience
ALIASES="${FILE_DIR}/.aliases"
if [ -e "$ALIASES" ]; then
	source "$ALIASES"
fi

# setup python startup script
PYTHONSTARTUP_FILE="${FILE_DIR}/.pythonstartup"
if [ -e "${PYTHONSTARTUP_FILE}" ]; then
	export PYTHONSTARTUP="${PYTHONSTARTUP_FILE}"
fi
