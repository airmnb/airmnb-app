
export DATABASE_URI=postgres://qstqzkzu:wIRQ-yASKMaE7hEdABZCD7cSKUuC40DA@stampy.db.elephantsql.com:5432/qstqzkzu
export WECHAT_APP_ID=wxb945640b6fd4a85b
export WECHAT_APP_SECRET=dc5b64195b959e8126d569b5fb96e425
# For non China
export HOST_DOMAIN_NAME=www.airmombaby.com

# # For China
# export HOST_DOMAIN_NAME=www.airmnb.com


FILE_DIR=$(dirname "${BASH_SOURCE}")

# load development environment
LOCAL_ENV="${FILE_DIR}/env"
if [ -e "${LOCAL_ENV}" ]; then
	source "${LOCAL_ENV}"
fi

echo -e "\033[1;32mDATABASE_URI: \033[0;36m${DATABASE_URI}\033[0m"
echo -e "\033[1;32mWECHAT_APP_ID: \033[0;36m${WECHAT_APP_ID}\033[0m"
echo -e "\033[1;32mWECHAT_APP_SECRET: \033[0;36m${WECHAT_APP_SECRET}\033[0m"
echo -e "\033[1;32mHOST_DOMAIN_NAME: \033[0;36m${HOST_DOMAIN_NAME}\033[0m"

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

