#
# Regular cron jobs for the dronevis package
#
0 4	* * *	root	[ -x /usr/bin/dronevis_maintenance ] && /usr/bin/dronevis_maintenance
