#!/usr/bin/env python3

import words

def words55(key, target='Reference'):
	return words.hmac(key, target, 55)

if __name__=='__main__':
	import sys
	import getpass

	try:
		master = getpass.getpass('Master: ')

		if len(sys.argv) < 2:
			while True:
				target = input("Service: ")

				if not target:
					break

				print(' '.join(words55(master, target)))
		elif len(sys.argv) == 2:
			print(' '.join(words55(master, sys.argv[1])))
		else:
			print('usage: ./words55.py <service>')
	except (KeyboardInterrupt, EOFError):
		print()
		pass

