SEARCH_PATTERN=$1
find . -name .repo -prune -o -name .git -prune -o -name out -prune -o  -type f | xargs grep $SEARCH_PATTERN --color 2>/dev/null
