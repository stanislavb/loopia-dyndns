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

FreeBSD License
===============

Copyright (c) 2013, Stanislav Blokhin (github.com/stanislavb)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
