#!/usr/bin/env python3

import os
import base64
import hashlib
import sys
import getpass

WORDS = [line.strip() for line in open('english.txt') if line.strip() != '']

# All the primes just less than a power of two encoded as:
# 2^key - value
PRIME_RESIDUALS = {
  8: 5,    9: 3,     10: 3,    11: 9,    12: 3,    13: 1,    14: 3,    15: 19,
 16: 15,   17: 1,    18: 5,    19: 1,    20: 3,    21: 9,    22: 3,    23: 15,
 24: 3,    25: 39,   26: 5,    27: 39,   28: 57,   29: 3,    30: 35,   31: 1,
 32: 5,    33: 9,    34: 41,   35: 31,   36: 5,    37: 25,   38: 45,   39: 7,
 40: 87,   41: 21,   42: 11,   43: 57,   44: 17,   45: 55,   46: 21,   47: 115,
 48: 59,   49: 81,   50: 27,   51: 129,  52: 47,   53: 111,  54: 33,   55: 55,
 56: 5,    57: 13,   58: 27,   59: 55,   60: 93,   61: 1,    62: 57,   63: 25,
 64: 59,   65: 49,   66: 5,    67: 19,   68: 23,   69: 19,   70: 35,   71: 231,
 72: 93,   73: 69,   74: 35,   75: 97,   76: 15,   77: 33,   78: 11,   79: 67,
 80: 65,   81: 51,   82: 57,   83: 55,   84: 35,   85: 19,   86: 35,   87: 67,
 88: 299,  89: 1,    90: 33,   91: 45,   92: 83,   93: 25,   94: 3,    95: 15,
 96: 17,   97: 141,  98: 51,   99: 115, 100: 15,  101: 69,  102: 33,  103: 97,
104: 17,  105: 13,  106: 117, 107: 1,   108: 59,  109: 31,  110: 21,  111: 37,
112: 75,  113: 133, 114: 11,  115: 67,  116: 3,   117: 279, 118: 5,   119: 69,
120: 119, 121: 73,  122: 3,   123: 67,  124: 59,  125: 9,   126: 137, 127: 1,
128: 159, 129: 25,  130: 5,   131: 69,  132: 347, 133: 99,  134: 45,  135: 45,
136: 113, 137: 13,  138: 105, 139: 187, 140: 27,  141: 9,   142: 111, 143: 69,
144: 83,  145: 151, 146: 153, 147: 145, 148: 167, 149: 31,  150: 3,   151: 195,
152: 17,  153: 69,  154: 243, 155: 31,  156: 143, 157: 19,  158: 15,  159: 91,
160: 47,  161: 159, 162: 101, 163: 55,  164: 63,  165: 25,  166: 5,   167: 135,
168: 257, 169: 643, 170: 143, 171: 19,  172: 95,  173: 55,  174: 3,   175: 229,
176: 233, 177: 339, 178: 41,  179: 49,  180: 47,  181: 165, 182: 161, 183: 147,
184: 33,  185: 303, 186: 371, 187: 85,  188: 125, 189: 25,  190: 11,  191: 19,
192: 237, 193: 31,  194: 33,  195: 135, 196: 15,  197: 75,  198: 17,  199: 49,
200: 75,  201: 55,  202: 183, 203: 159, 204: 167, 205: 81,  206: 5,   207: 91,
208: 299, 209: 33,  210: 47,  211: 175, 212: 23,  213: 3,   214: 185, 215: 157,
216: 377, 217: 61,  218: 33,  219: 121, 220: 77,  221: 3,   222: 117, 223: 235,
224: 63,  225: 49,  226: 5,   227: 405, 228: 93,  229: 91,  230: 27,  231: 165,
232: 567, 233: 3,   234: 83,  235: 15,  236: 209, 237: 181, 238: 161, 239: 87,
240: 467, 241: 39,  242: 63,  243: 9,   244: 189, 245: 163, 246: 107, 247: 81,
248: 237, 249: 75,  250: 207, 251: 9,   252: 129, 253: 273, 254: 245, 255: 19
}

def prime(bits):
	bits = int(bits)
	if bits < 8:
		bits = 8
	if bits > 255:
		bits = 255
	return (1 << bits) - PRIME_RESIDUALS[bits]

def prime_truncate(x, bits):
	return x % prime(bits)

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

	entropy = int(entropy)
	if entropy < 0:
		raise ValueError('negitive entropy?')

	if entropy == 0:
		return (words[0], )

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

def ss64_word(master, target='amazon', words=None):
	bits = 48
	password = '%s:%s' % (master, target)
	digest = hashlib.sha256(password.encode('utf8')).digest()
	value = prime_truncate(int.from_bytes(digest, byteorder='big'), bits)
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

