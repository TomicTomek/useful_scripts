PATTERN=$1
if [ -z $PATTERN ]; then
    echo "You are stupid, give me a pattern!"
    exit
fi
PROCESS_NAME=`adb shell ps | grep $PATTERN  | awk '{print $9}'`
PROCESS_PID=`adb shell ps | grep $PATTERN  | awk '{print $2}'`

echo "uptime of:  $PROCESS_NAME"
adb shell ps -o etime= -p $PROCESS_PID
