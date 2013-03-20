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
	logger.debug("Result: %s", r.text)
	return r.text

def resolve_host(hostname)
	try:
		ip = gethostbyname(hostname)
		return ip
	except gaierror:
		logger.debug("Couldn't resolve hostname: %s", hostname)
		return None

def read_config(file=configfile):
	cleanconfig = {}
	config = configparser.ConfigParser()
	config.read(file)

	for domain in config.keys():
		keys = config[domain].keys()
		# We skip the DEFAULT section and make sure username, password and ip values are available
		if 'DEFAULT' not in domain and 'ip' in keys and 'username' in keys and 'password' in keys:
			cleanconfig[domain] = config[domain]
	return cleanconfig


def init():
	config = read_config(configfile)
	for domain in config.keys():
		futureip = config[domain][ip]
		username = config[domain][username]
		password = config[domain][password]
		
		if 'check' in futureip:
			futureip = get_my_ip()

		currentip = resolve_host(domain)
		if futureip is in currentip:
			logger.info("%s: Already correct IP", domain)
		else:
			ret = update_dns_record(domain, username, password, ip)
		        if 'BADAUTH' is in ret:
				logger.info("%s: Bad Credentials", domain)
			if 'abuse' is in ret:
				logger.info("%s: Update abuse", domain)
			if 'nochg' is in ret:
				logger.info("%s: No change", domain)
			if 'good' is in ret:
				logger.info("%s: Went well", domain)
			else:
				logger.info("%s: %s", domain, ret)
