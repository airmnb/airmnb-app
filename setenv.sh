
export AMB_DATABASE_URI=postgres://*
# For non China
export AMB_DOMAIN_NAME=

export AMB_FACEBOOK_APP_KEY=
export AMB_FACEBOOK_APP_SECRET=
export AMB_FACEBOOK_AUTHORIZE_URL=https://www.facebook.com/dialog/oauth
export AMB_FACEBOOK_ACCESS_TOKEN_URL=/oauth/access_token

export AMB_GOOGLE_APP_KEY=
export AMB_GOOGLE_APP_SECRET=
export AMB_GOOGLE_AUTHORIZE_URL=https://accounts.google.com/o/oauth2/v2/auth
export AMB_GOOGLE_ACCESS_TOKEN_URL=https://www.googleapis.com/oauth2/v4/token

export AMB_WECHAT_APP_KEY=
export AMB_WECHAT_APP_SECRET=

export AMB_WEAPP_APP_ID=
export AMB_WEAPP_APP_SECRET=

FILE_DIR=$(dirname "${BASH_SOURCE}")

#
# load development settings from `env` if it exists
#
LOCAL_ENV="${FILE_DIR}/env"
if [ -e "${LOCAL_ENV}" ]; then
	source "${LOCAL_ENV}"
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
