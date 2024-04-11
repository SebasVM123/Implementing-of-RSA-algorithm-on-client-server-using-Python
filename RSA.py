from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes

n_bits = 18


def extended_euclidean_algorithm(a, b):
    g = [b, a]
    u = [1, 0]
    v = [0, 1]

    i = 1

    while g[i] != 0:
        y = int(g[i - 1] / g[i])
        next_g = g[i - 1] - (y * g[i])
        next_u = u[i - 1] - (y * u[i])
        next_v = v[i - 1] - (y * v[i])
        g.append(next_g)
        u.append(next_u)
        v.append(next_v)
        i += 1

    if v[i - 1] < 0:
        v[i - 1] += b

    x = v[i - 1]
    return x


class RSA:
    def __init__(self, e=65537):
        self.e = e
        p, q = self.generate_prime_numbers()
        self.n = p * q
        phi_n = (p - 1) * (q - 1)

        self.private_key = self.generate_private_key(phi_n)

    def generate_prime_numbers(self):
        p = number.getPrime(int(n_bits/2))
        q = number.getPrime(int(n_bits/2))

        while p == q:
            p = number.getPrime(int(n_bits/2))
            q = number.getPrime(int(n_bits/2))

        while self.e % (p - 1) == 0:
            p = number.getPrime(int(n_bits/2))

        while self.e % (q - 1) == 0:
            q = number.getPrime(int(n_bits/2))

        return p, q

    def generate_private_key(self, phi_n):
        d = extended_euclidean_algorithm(self.e, phi_n)
        return d

    def decrypt(self, crypto_message):
        c = crypto_message
        m = (c ** self.private_key) % self.n
        return m

    def get_public_key(self):
        return self.e, self.n

    @staticmethod
    def encrypt(message, public_key):
        e = public_key[0]
        n = public_key[1]
        int_message = bytes_to_long(message)
        c = (int_message ** e) % n
        return c


rsa = RSA(e=65537)
