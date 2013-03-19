#!/usr/bin/env python
# Authors: Stanislav Blokhin

import requests
from re import search
import logger
import configparser
from socket import gethostbyname, gaierror

configfile="accounts.cfg"

#
# Uses Loopia's external IP checker, returns IP address string if it goes well
#
def get_my_ip():
	ipcheck = 'http://dns.loopia.se/checkip/checkip.php'
	r = requests.get(ipcheck)
	logger.info(r.text)
	# Simple IP address regexp, matches some invalid addresses too.
	m = search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', r.text)
	return m.group(0)

#
# Sends a GET request to Loopia's DynDNS to update IP address.
# If address is omitted, tries to map its own public IP to the hostname.
#
def update_dns_record(hostname, username, password, ip = get_my_ip()):
	dyndns = 'http://dns.loopia.se/XDynDNSServer/XDynDNS.php'
	if not ip:
		return False
	logger.info("Trying to make %s point to %s", hostname, ip)
	payload = {'system': 'custom', 'hostname': hostname, 'myip': ip, 'backmx': 'YES'}
	r = requests.get(dyndns, params=payload, auth=(username, password))
	logger.info("Result: %s", r.text)
        if 'BADAUTH' is in r.text:
		logger.info("bad credentials")
	if 'abuse' is in r.text:
		logger.info("Update abuse")
	if 'nochg' is in r.text:
		logger.info("No change")
	if 'good' is in r.text:
		logger.info("Went well")
	return r.text

def resolvehost(hostname)
	try:
		gethostbyname(hostname)
	except gaierror:
		logger.debug("resolvehost(): Couldn't resolve %s", hostname)
		return None

def loadconfig(file=configfile):
	config = configparser.ConfigParser()
	config.read(file)
