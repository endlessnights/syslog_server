# syslog_server

Collects data from Mikrikt (RouterOS) system logs, configured to collect and process L2TP-clients:

It writes to logs/<filename>.logs:
date/time, l2tp-secret-name, src-local-address->dst-address:dst-port
