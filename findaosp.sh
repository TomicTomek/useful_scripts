FILE_PATTERN=$1
SEARCH_PATTERN=$2
find . -name .repo -prune -o -name .git -prune -o -name out -prune -o  -type f -name $FILE_PATTERN | xargs grep $SEARCH_PATTERN --color 2>/dev/null
