#!/usr/bin/env python3

import os
import base64
import hashlib
import sys
import getpass

WORDS = [line.strip() for line in open('english.txt') if line.strip() != '']

def pick_word(words=None):
	if words is None:
		words = WORDS
	x = len(words) + 1
	while x >= len(words):
		x = int.from_bytes(os.urandom((len(bin(len(words))) + 5) // 8),
				   byteorder='big')
	return words[x]

def gen_password(entropy=60, words=None):
	if words is None:
		words = WORDS
	entropy_words = int(entropy / (len(bin((len(words)))) - 2) + .5)
	return tuple(pick_word(words) for _ in range(entropy_words))

def ss64(master, target='amazon'):
	phrase = '%s:%s' % (master, target)
	digest = hashlib.sha256(phrase.encode('utf8')).digest()
	return base64.b64encode(digest).decode('ascii')[:20]		\
	       .replace('+', 'E').replace('/', 'a')

if __name__=='__main__':
	if len(sys.argv) == 2:
		master = getpass.getpass('Master: ')
		print(ss64(master, sys.argv[1]))
	elif len(sys.argv) == 1:
		print(' '.join(gen_password()))
	else:
		print('usage: password.py <service name> or password.py')
