anallan
-------

Display existing IPv4 and IPv6 computers on your LAN and their NetBios names.
Useful if you are hunting for rogue IP numbers or want a mapping between
ipv4/ipv6/NetBios numbers and names.

Living hosts are displayed in ASCII-art 2D map, so you can at a glance assess
the status of your network.

Prerequisities
--------------

You need python3 to run the program.

To discover hosts on ipv6 network, `ping6` (part of iputils) is recommended. If
missing, most likely only a few ipv6 hosts will be discovered.

ipv4 part of the code (interface address discovery) is quite Linux specifics.

If you want to scan NetBios machines (AKA MS Windows netword), you must install
either `nbmlookup` (part of SAMBA) or (recommended) `nmbscan`. `nmbscan` is
available at http://nmbscan.g76r.eu/


Work in progress, use at your own discretion !!!
