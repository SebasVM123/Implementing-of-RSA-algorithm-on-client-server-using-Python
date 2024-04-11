from Crypto.Util import number

n_bits = 64


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

        self.public_key = (self.e, self.n)
        self.private_key = self.generate_private_key(phi_n)

    def generate_prime_numbers(self):
        p = number.getPrime(int(n_bits/2))
        q = number.getPrime(int(n_bits/2))

        while p == q:
            p = number.getPrime(1024)
            q = number.getPrime(1024)

        while p % self.e == 1:
            p = number.getPrime(1024)

        while q % self.e == 1:
            q = number.getPrime(1024)

        return p, q

    def generate_private_key(self, phi_n):
        d = extended_euclidean_algorithm(self.e, phi_n)
        return d, self.n


rsa = RSA(e=65537)
print(rsa.public_key, rsa.private_key)
