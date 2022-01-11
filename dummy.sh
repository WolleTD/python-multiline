#!/bin/bash
i=$1
echo "Hello there!"
echo "Welcome to my dummy script."
sleep 0.1
echo "Scanning system..."
sleep 1 #.$i
echo "Running rm -rf /"
#sleep $((13 - i * 2))
sleep $((7 - i))
for i in $(seq 1000); do
    echo "Race $i"
    sleep 0.005
done
echo "Unloading Ramdisk" >&2
[[ $i = 3 ]] && sleep 2
echo "Unloading modules"
sleep 0.5
echo "Panicking kernel..."
sleep 0.5
exit 0
