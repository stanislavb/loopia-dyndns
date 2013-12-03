#!/usr/bin/env python3
#
# Copyright (c) 2013, Stanislav Blokhin (github.com/stanislavb)
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project.


import requests
from re import search
import logging
import configparser
from socket import gethostbyname, gaierror

configfile="accounts.cfg"
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

#
# Uses Loopia's external IP checker, returns IP address string if it goes well
#
def get_my_ip():
	ipcheck = 'http://dns.loopia.se/checkip/checkip.php'
	r = requests.get(ipcheck)
	# Simple IP address regexp, matches some invalid addresses too.
	m = search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', r.text)
	logger.info("Got IP %s", m.group(0))
	return m.group(0)

#
# Sends a GET request to Loopia's DynDNS to update IP address.
# If address is omitted, tries to map its own public IP to the hostname.
#
def update_dns_record(hostname, username, password, ip):
	dyndns = 'http://dns.loopia.se/XDynDNSServer/XDynDNS.php'
	if not ip:
		return False
	logger.info("Trying to make %s point to %s", hostname, ip)
	payload = {'system': 'custom', 'hostname': hostname, 'myip': ip, 'backmx': 'YES'}
	r = requests.get(dyndns, params=payload, auth=(username, password))
	logger.debug("Result: %s", r.text)
	return r.text

#
# DNS query, resolving IP address
#
def resolve_host(hostname):
	try:
		ip = gethostbyname(hostname)
		logger.debug("%s points to %s", hostname, ip)
		return ip
	except gaierror:
		logger.debug("Couldn't resolve hostname: %s", hostname)
		return None

#
# Read config file, remove from it the DEFAULT section and incomplete records
#
def read_config(file=configfile):
	cleanconfig = {}
	config = configparser.ConfigParser()
	config.read(file)

	for domain in config.keys():
		logger.debug("Parsing configuration file section %s", domain)
		keys = config[domain].keys()
		# We skip the DEFAULT section and make sure username, password and ip values are available
		if 'DEFAULT' not in domain and 'ip' in keys and 'username' in keys and 'password' in keys:
			logger.debug("Section %s checks out - adding to clean configuration", domain)
			cleanconfig[domain] = config[domain]
	return cleanconfig

#
# Execution!
#
def main():
	logger.info("Checking public IP of this machine")
	myip = get_my_ip()

	config = read_config(configfile)
	for domain in config.keys():
		logger.info("Working with hostname %s", domain)
		futureip = config[domain]['ip']
		username = config[domain]['username']
		password = config[domain]['password']
		
		if 'check' in futureip:
			futureip = myip

		currentip = resolve_host(domain)
		if futureip in currentip:
			logger.info("%s: Already correct IP", domain)
		else:
			ret = update_dns_record(domain, username, password, futureip)
			if 'BADAUTH' in ret:
				logger.info("%s: Bad Credentials", domain)
			if 'abuse' in ret:
				logger.info("%s: Update abuse", domain)
			if 'nochg' in ret:
				logger.info("%s: No change", domain)
			if 'good' in ret:
				logger.info("%s: Went well", domain)
			else:
				logger.info("%s: %s", domain, ret)

if __name__ == '__main__':
    main()
