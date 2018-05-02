
export AMB_DATABASE_URI=postgres://qstqzkzu:wIRQ-yASKMaE7hEdABZCD7cSKUuC40DA@stampy.db.elephantsql.com:5432/qstqzkzu
export AMB_WECHAT_APP_ID=wxb945640b6fd4a85b
export AMB_WECHAT_APP_SECRET=dc5b64195b959e8126d569b5fb96e425
# For non China
export AMB_DOMAIN_NAME=www.airmombaby.com

export AMB_FACEBOOK_APP_KEY=100732940275183
export AMB_FACEBOOK_APP_SECRET=d3cec74fd9e331fed0d22ef9c00b93dc
export AMB_FACEBOOK_AUTHORIZE_URL=https://www.facebook.com/dialog/oauth
export AMB_FACEBOOK_ACCESS_TOKEN_URL=/oauth/access_token

export AMB_GOOGLE_APP_KEY=372339553651.apps.googleusercontent.com
export AMB_GOOGLE_APP_SECRET=yZjP1B_oofR451Nee8zOefcr
export AMB_GOOGLE_AUTHORIZE_URL=https://accounts.google.com/o/oauth2/v2/auth
export AMB_GOOGLE_ACCESS_TOKEN_URL=https://www.googleapis.com/oauth2/v4/token

export AMB_WECHAT_APP_KEY=wxb45fa53ae00e3b16
export AMB_WECHAT_APP_SECRET=042f0fed3930591f05b6440663720d9c


# # For China
# export AMB_DOMAIN_NAME=www.airmnb.com


FILE_DIR=$(dirname "${BASH_SOURCE}")

# load development environment
LOCAL_ENV="${FILE_DIR}/env"
if [ -e "${LOCAL_ENV}" ]; then
	source "${LOCAL_ENV}"
fi

echo -e "\033[1;32mAMB_DATABASE_URI: \033[0;36m${AMB_DATABASE_URI}\033[0m"
echo -e "\033[1;32mAMB_WECHAT_APP_ID: \033[0;36m${AMB_WECHAT_APP_ID}\033[0m"
echo -e "\033[1;32mAMB_WECHAT_APP_SECRET: \033[0;36m${AMB_WECHAT_APP_SECRET}\033[0m"
echo -e "\033[1;32mAMB_DOMAIN_NAME: \033[0;36m${AMB_DOMAIN_NAME}\033[0m"

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

