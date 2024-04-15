from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes

key_size = 2048
FORMAT = 'UTF-8'


def extended_euclidean_algorithm(a, b):
    g = [b, a]
    u = [1, 0]
    v = [0, 1]

    i = 1

    while g[i] != 0:
        y = g[i - 1] // g[i]
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
        p = number.getPrime(key_size // 2)
        q = number.getPrime(key_size // 2)

        while p == q:
            p = number.getPrime(int(key_size / 2))
            q = number.getPrime(int(key_size / 2))

        while self.e % (p - 1) == 0:
            p = number.getPrime(int(key_size / 2))

        while self.e % (q - 1) == 0:
            q = number.getPrime(int(key_size / 2))

        return p, q

    def generate_private_key(self, phi_n):
        d = number.inverse(self.e, phi_n)
        return d

    def get_public_key(self):
        return self.e, self.n

    def get_private_key(self):
        return self.private_key

    @staticmethod
    def encrypt(m, public_key):
        e = public_key[0]
        n = public_key[1]
        c = pow(m, e, n)
        return c

    def decrypt(self, crypto_message):
        c = crypto_message
        m = pow(c, self.private_key, self.n)
        return m


'''rsa = RSA()
rsa2 = RSA()

c_1 = rsa2.encrypt(5000, rsa.get_public_key())
m_1 = rsa.decrypt(c_1)

print(m_1)'''
