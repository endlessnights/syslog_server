# syslog_server

Collects data from Mikrotik (RouterOS) system logs, configured to collect and process L2TP-clients:

It writes to logs/<filename>.logs:
date/time, l2tp-secret-name, src-local-address->dst-address:dst-port

Mangle rule for this syslog server:

/ip firewall mangle add action=log chain=prerouting connection-state=new dst-address-list=!DontLog in-interface=!ether1 log=yes log-prefix=LOG_USERS protocol=tcp src-addr
ess=192.168.40.0/22 tcp-flags=syn

Where 192.168.40.0/22 - l2tp user network
dst-address-list "DontLog" - public DNSs i.e. 1.1.1.1, 8.8.8.8, 8.8.4.4 etc.

Configured via System>Logging>Remote
