FILE_DIR=$(dirname "${BASH_SOURCE}")
#
# load development settings from `env` if it exists
#
LOCAL_ENV="${FILE_DIR}/env"
if [ -e "${LOCAL_ENV}" ]; then
	source "${LOCAL_ENV}"
else
	echo -e "\033[0;31m${LOCAL_ENV} isn't configured.\033[0m"
	return
fi

echo -e "\033[1;32mAMB_DATABASE_URI: \033[0;36m${AMB_DATABASE_URI}\033[0m"
echo -e "\033[1;32mAMB_DOMAIN_NAME: \033[0;36m${AMB_DOMAIN_NAME}\033[0m"

#
# load aliases for convenience if exists
#
ALIASES="${FILE_DIR}/.aliases"
if [ -e "$ALIASES" ]; then
	source "$ALIASES"
fi

#
# setup python startup script if exists
#
PYTHONSTARTUP_FILE="${FILE_DIR}/.pythonstartup"
if [ -e "${PYTHONSTARTUP_FILE}" ]; then
	export PYTHONSTARTUP="${PYTHONSTARTUP_FILE}"
fi
