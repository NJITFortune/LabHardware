#/bin/sh

echo "10s preview of camera $1 at distance $2"
sleep 1

if [ $1 = 0 ]
then
	i2cset -y 10 0x24 0x24 0x02
fi
if [ $1 = 1 ]
then	
	i2cset -y 10 0x24 0x24 0x12
fi 
if [ $1 = 2 ]
then
	i2cset -y 10 0x24 0x24 0x22
fi
if [ $1 = 3 ]
then
	i2cset -y 10 0x24 0x24 0x32
fi

libcamera-still -t 10000 --autofocus-mode=manual --lens-position=$2
