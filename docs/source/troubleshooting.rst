.. _troubleshooting:

#################
 Troubleshooting
#################

*************
 Rate Limits
*************

|  Warframe Market's server imposes a limit on the number of requests that a
   user can perform per second. The exact number is not concrete, but it ranges from 3–5 requests per second.

|  WarMAC typically makes 2 requests to WFM per execution: one to collect data
   about the item itself, and a second to collect relevant user orders. This
   means that you, the end-user, can run WarMAC twice per second.

======================================
 I'm still rate-limited after waiting
======================================

|  If you are still rate-limited after waiting for minutes on end to make
   another request, please file an issue on `GitHub <https://github.com/Eutropios/WarMAC/issues>`_.
