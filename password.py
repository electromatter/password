#!/usr/bin/env python3

import os
import base64
import hashlib
import sys
import getpass

WORDS = [line.strip() for line in open('english.txt') if line.strip() != '']

def truncate_bits(x, bits):
	return x & ((1 << bits) - 1)

def secure_random_int(bits):
	x = int.from_bytes(os.urandom((bits + 7) // 8), byteorder='big')
	return truncate_bits(x, bits)

def pick_word(words=None):
	if words is None:
		words = WORDS
	bits = len(bin(len(words))) - 2
	x = len(words) + 1
	while x >= len(words):
		x = secure_random_int(bits)
	return words[x]

def gen_password(entropy=60, words=None):
	if words is None:
		words = WORDS

	if len(words) < 2:
		raise ValueError('alphabet has no non-zero elements')

	entropy_words = int(entropy / (len(bin((len(words)))) - 2) + .5)
	return tuple(pick_word(words) for _ in range(entropy_words))

def int_as_words(x, words=None):
	if words is None:
		words = WORDS

	if x == 0:
		return words[0]

	if len(words) < 2:
		raise ValueError('alphabet has no non-zero elements')

	phrase = []
	while x > 0:
		phrase.append(words[x % len(words)])
		x //= len(words)

	return tuple(reversed(phrase))

def words_as_int(phrase, words=None):
	if words is None:
		words = WORDS

	if len(words) < 2:
		raise ValueError('alphabet has no non-zero elements')

	x = 0
	for word in phrase:
		x *= len(words)
		x += words.index(word)

	return x

def ss64_word(master, target='amazon', words=None, bits=40):
	password = '%s:%s' % (master, target)
	digest = hashlib.sha256(password.encode('utf8')).digest()
	value = truncate_bits(int(digest, byteorder='big'), bits)
	return int_as_words(value, words)

def ss64(master, target='amazon'):
	password = '%s:%s' % (master, target)
	digest = hashlib.sha256(password.encode('utf8')).digest()
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

