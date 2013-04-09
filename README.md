Loopia DynDNS
=============

Updates DNS records hosted at Loopia, a swedish hosting provider with its own implementation of DynDNS.

Requirements
============
* Python 3
* Requests library for python 3

Config file
===========
Defaults under [DEFAULT] tag are inherited unless overridden. The "check" value makes the script check for the public IP of the machine it is run on using Loopia's IP checker. If it run behind NAT, it will get the public IP of the router.

<pre>
[DEFAULT]
username = example.com
password = britneyspears
ip = check

[example.com]
ip = check

[www.example.com]
ip = check

[other.example.com]
ip = 1.2.3.4
</pre>

Usage
=====

The loopiadns.py script contains one config line. By default it points to accounts.cfg file in the same directory as the script.
<pre>
configfile="accounts.cfg"
</pre>

Run the script with a correctly written config file in the right location and you will get an output telling you what happened. Take care not to run it too often or face restrictions from Loopia's DynDNS service. When output is "abuse", wait for an hour or so before trying again.
