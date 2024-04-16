from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes

key_size = 2048
FORMAT = 'UTF-8'

#El algoritmo de euclides extendido se utiliza para encontrar el inverso multiplicativo de dos números 
#enteros a y b, es decir, un número x tal que (a*x) % b = 1
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
    #Se utiliza el valor e=65537 por defecto, ya que es un número primo y es el más comúnmente utilizado, 
    #se debe cumplir que 1 < e < phi_n y que e y phi_n sean coprimos
    #se calcula n = p*q y phi_n = (p-1)*(q-1)
    #Se calcula la clave privada d utilizando el algoritmo de euclides extendido
    def __init__(self, e=65537):
        self.e = e
        p, q = self.generate_prime_numbers()
        self.n = p * q
        phi_n = (p - 1) * (q - 1)
        self.private_key = self.generate_private_key(phi_n)

    #Se generan dos números primos p y q, tienen un tamaño de key_size/2 pues al multiplicarse se obtiene 
    #un número de tamaño key_size
    def generate_prime_numbers(self):
        p = number.getPrime(key_size // 2)
        q = number.getPrime(key_size // 2)

        #Se verifica que p y q sean diferentes
        while p == q:
            p = number.getPrime(int(key_size / 2))
            q = number.getPrime(int(key_size / 2))

        #Se verifica que (p-1)*(q-1) no sea modulo de e
        while ((p - 1) * (q - 1)) % self.e == 0:
            p = number.getPrime(int(key_size / 2))
            q = number.getPrime(int(key_size / 2))

        return p, q

    #Se calcula la clave privada d utilizando el algoritmo de euclides extendido
    def generate_private_key(self, phi_n):
        d = extended_euclidean_algorithm(self.e, phi_n)
        return d

    #Se obtiene la clave publica 
    def get_public_key(self):
        return self.e, self.n
    
    #Se obtiene la clave privada
    def get_private_key(self):
        return self.private_key

    #Se encripta el mensaje m utilizando la clave publica
    #como public_key = (e, n), se extrae e y n para realizar el calculo
    #Se convierte el mensaje m a un entero y se calcula c = m^e mod n
    @staticmethod
    def encrypt(m, public_key):
        e = public_key[0]
        n = public_key[1]
        int_m = bytes_to_long(m.encode(FORMAT))
        c = pow(int_m, e, n)
        return c

    #Se recibe el mensaje encriptado c y se calcula m = c^d mod n
    #Se convierte el entero m a un string con FORMAT = 'UTF-8'
    def decrypt(self, crypto_message):
        c = crypto_message
        m_int = pow(c, self.private_key, self.n)
        m = long_to_bytes(m_int).decode(FORMAT)
        return m


#Prueba de la clase RSA
'''rsa = RSA()
rsa2 = RSA()

c_1 = rsa2.encrypt('holaaaa', rsa.get_public_key())
m_1 = rsa.decrypt(c_1)

print(m_1)'''
