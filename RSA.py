from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes

key_size = 2048
FORMAT = 'UTF-8'


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
        int_m = bytes_to_long(m.encode(FORMAT))
        c = pow(int_m, e, n)
        return c

    def decrypt(self, crypto_message):
        c = crypto_message
        m_int = pow(c, self.private_key, self.n)
        m = long_to_bytes(m_int).decode(FORMAT)
        return m


'''rsa = RSA()
rsa2 = RSA()

c_1 = rsa2.encrypt('h', rsa.get_public_key())
m_1 = rsa.decrypt(c_1)

print(m_1)'''
