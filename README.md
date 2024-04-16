# Implementing-of-RSA-algorithm-on-client-server-using-Python
# RSA.py
## Descripción:
El archivo RSA.py implementa el algoritmo RSA (Rivest-Shamir-Adleman) utilizado en criptografía asimétrica para la generación de claves públicas y privadas, así como el cifrado y descifrado de mensajes.

## Funcionalidades:
- **Generación de Claves RSA:**
  - Inicialización automática de claves pública y privada RSA al instanciar la clase `RSA`.
  - Generación de números primos `p` y `q` para formar la clave pública y privada.

- **Cifrado y Descifrado:**
  - Método estático `encrypt` para cifrar mensajes utilizando la clave pública.
  - Método `decrypt` para descifrar mensajes utilizando la clave privada.

# Cliente.py
## Descripción:
El archivo Cliente.py implementa un cliente de chat para comunicarse con un servidor utilizando sockets TCP/IP y cifrado RSA para garantizar la seguridad de las comunicaciones.

## Funcionalidades:
- **Inicio de Sesión:**
  - Interfaz gráfica para iniciar sesión con un nombre de usuario.
  - Conexión al servidor y gestión de errores.

- **Interfaz de Chat:**
  - Interfaz gráfica para enviar y recibir mensajes encriptados.
  - Envío de mensajes a todos los usuarios conectados o a usuarios específicos.

- **Comunicación Segura:**
  - Cifrado RSA de mensajes antes de enviarlos al servidor.
  - Descifrado RSA de mensajes recibidos del servidor.

# Servidor.py
## Descripción:
El archivo Servidor.py implementa un servidor de chat que acepta conexiones de múltiples clientes, gestiona la comunicación entre ellos y utiliza el cifrado RSA para asegurar las comunicaciones.

## Funcionalidades:
- **Gestión de Conexiones:**
  - Acepta conexiones de clientes utilizando sockets TCP/IP.
  - Registra clientes conectados y maneja la comunicación entre ellos.

- **Interfaz de Administración:**
  - Interfaz gráfica para administrar la comunicación del servidor.
  - Permite enviar mensajes a todos los clientes o a clientes específicos.

- **Seguridad con RSA:**
  - Utiliza cifrado RSA para encriptar mensajes antes de enviarlos a los clientes.
  - Descifra mensajes cifrados recibidos de los clientes utilizando RSA.

## Uso

1. **Clonar el Repositorio:**
   - Para clonar el repositorio, utiliza el siguiente comando en la terminal:
     ```bash
     git clone https://github.com/SebasVM123/Implementing-of-RSA-algorithm-on-client-server-using-Python.git
     ```
     Reemplaza `tu-usuario` con tu nombre de usuario en GitHub y `nombre-repositorio` con el nombre de tu repositorio.

2. **Ejecutar el Proyecto:**
   - Accede al directorio del repositorio clonado:
     ```bash
     cd nombre-repositorio
     ```
   - Si el proyecto tiene dependencias, instálalas utilizando el gestor de paquetes correspondiente (por ejemplo, pip en Python):
     ```bash
     pip install -r requirements.txt
     ```
   - Ejecuta el proyecto principal (por ejemplo, `main.py`) para iniciar la aplicación:
     ```bash
     python main.py
     ```
     Reemplaza `main.py` con el nombre del archivo principal de tu aplicación si es diferente.

## Contribuyentes

Agradecimientos a los contribuyentes que han participado en el desarrollo del proyecto.

- [Brandon Castaño](https://github.com/bcg733)
- [Juan P. Cataño](https://github.com/juan-npablo)
- [Gerwin Lambraño](https://github.com/gerwintorres)
- [Sebastian Velásquez](https://github.com/SebasVM123)
## Licencia

Este proyecto está bajo la Licencia [Nombre de la licencia]. Consulta el archivo [LICENSE](LICENSE) para más detalles.
