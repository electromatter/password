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
	value = 0
	resid = 1
	for c in coeff:
		value = (value + c * resid) % prime
		resid = (resid * x) % prime
	return value

def gen_poly(prime, secret, m):
	if isinstance(secret, str):
		secret = secret.encode('utf8')

	if isinstance(secret, bytes):
		secret = int.from_bytes(secret, byteorder='big')

	if secret >= prime:
		raise ValueError('Secret is unrecoverable under selected prime. (secret is too large)')

	if m < 1:
		raise ValueError('Secret is unrecoverable. (no shares)')

	if m < 2:
		raise ValueError('Shamir reduces to identity under one share.')

	return [secret] + [random_int(prime) for _ in range(m - 1)]

def gen_shares(prime, secret, n, m):
	if n < m:
		raise ValueError('Secret is unrecoverable. (too many shares required)')

	if n >= prime:
		raise ValueError('Prime too small for the desired number of shares.')

	coeff = gen_poly(prime, secret, n, m)
	return [(x, eval_poly(prime, coeff, x)) for x in range(1, n + 1)]

def recover(prime, shares):
	shares = set((x % prime, y % prime) for x, y in shares)

	if len(shares) != len(set(next(zip(*shares)))):
		raise ValueError('Duplicated x value.')

	value = 0
	for x_0, y_0 in shares:
		product = 1
		for x, _ in shares:
			if x == x_0:
				continue
			product = (product * x * modinv((x - x_0) % prime, prime)) % prime
		value = (value + y_0 * product) % prime

	return value
