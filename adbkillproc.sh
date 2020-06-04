adb root
adb shell kill -9 `adb shell ps | grep $1 | awk '{print $2}'`
