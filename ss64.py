#!/usr/bin/env python3

def ss64(master, target='amazon'):
	password = '%s:%s' % (master, target)
	digest = hashlib.sha256(password.encode('utf8')).digest()
	return base64.b64encode(digest).decode('ascii')[:20]		\
	       .replace('+', 'E').replace('/', 'a')

if __name__=='__main__':
	if len(sys.argv) == 2:
		target = input('Service: ')
		master = getpass.getpass('Master: ')
		print(ss64(master, target))
	if len(sys.argv) == 3:
		target = sys.argv[2]
		master = getpass.getpass('Master: ')
		print(ss64(master, target))
	else:
		print('usage: ss64.py <service name>')
