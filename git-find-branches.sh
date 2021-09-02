FIND_PATTERN=$1
find . -name "*.git" -type d | xargs dirname | xargs -I{} sh -c 'if [ ! -z "$(git -C {} branch --list | grep '$FIND_PATTERN')" ]; then realpath {}; git -C {} branch --list | grep '$FIND_PATTERN'; echo ""; fi' 2>/dev/null
