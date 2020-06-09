PATTERN=$1
if [ -z $PATTERN ]; then
    echo "You are stupid, give me a pattern!"
    exit
fi
adb shell dumpsys activity activities | sed -En -e '/Running activities/,/Run #0/p' | grep  $PATTERN