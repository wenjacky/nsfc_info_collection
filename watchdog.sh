#!/bin/bash

#wenjigang 20180502

source /etc/profile
source /etc/bashrc
source ~/.bash_profile
source ~/.bashrc

export PATH=$PATH:/home/wenjigang/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

echo `whoami`
echo "$PATH"

while((1)); do
adin=`ps aux |grep auto_search.py |wc -l`
index=`cat /home/wenjigang/auto_search/done.txt`

if [ "$adin" != '2' ];then
	echo "auto_search.py is not running. try to start..."
	cd /home/wenjigang/auto_search
	pkill firefox
	/usr/bin/python auto_search.py &
else
	echo "auto_search watchdog is running:"+$adin
fi

sleep 60

done
