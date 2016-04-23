#!/usr/bin/env python3

import base64
import hashlib
import sys
import getpass

def ss64(master, target='amazon'):
	password = '%s:%s' % (master, target)
	digest = hashlib.sha256(password.encode('utf8')).digest()
	return base64.b64encode(digest).decode('ascii')[:20]		\
	       .replace('+', 'E').replace('/', 'a')

if __name__=='__main__':
	if len(sys.argv) == 2:
		target = sys.argv[1]
		master = getpass.getpass('Master: ')
		print(ss64(master, target))
	else:
		print('usage: ss64.py <service name>')
