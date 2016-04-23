#!/usr/bin/env python3

from words import prime, random_int

def egcd(b, n):
	x0, x1, y0, y1 = 1, 0, 0, 1
	while n != 0:
		q, b, n = b // n, n, b % n
		x0, x1 = x1, x0 - q * x1
		y0, y1 = y1, y0 - q * y1
	return  b, x0, y0

def modinv(b, n):
	g, x, _ = egcd(b, n)
	if g != 1:
		raise ValueError('%r is not invertable mod %r' % (b, n))
	return x % n

def eval_poly(prime, coeff, x):
	pass

def gen_shares(prime, secret, n, m):
	if isinstance(secret, str):
		secret = secret.encode('utf8')

	if isinstance(secret, bytes):
		secret = int.from_bytes(secret, byteorder='big')

	if secret >= prime:
		raise ValueError('secret is ambiguous under prime')

	if n < m or n < 2:
		raise ValueError('invalid number of shares')

	coeff = [secret] + [random_int(prime) for _ in range(m - 1)]

	return [(x, eval_poly(prime, coeff, x)) for x in range(1, n + 1)]

def recover(prime, shares):
	shares = set(shares)

	if len(shares) != len(set(zip(*shares)[0])):
		raise ValueError('invalid shares - non-univalent')

	value = 0
	for x_0, y_0 in shares:
		product = 1
		for x, _ in shares:
			product = (product * x * modinv((x - x_0) % prime, prime)) % prime
		value = (value + y_0 * product) % prime

	return value
