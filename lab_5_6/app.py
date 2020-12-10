from flask import Flask, request, make_response
import string
from pony.flask import Pony
from pony.orm import Required, Database, Optional
from Crypto.Protocol.KDF import bcrypt, bcrypt_check
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import ssl


app = Flask(__name__)
app.config['PONY'] = {
  'provider': 'mysql',
  'host': '127.0.0.1',
  'user': 'vasniktel',
  'passwd': 'vasniktel',
  'db': 'crypto_lab_5'
}

db = Database()
Pony(app)


class User(db.Entity):
  login = Required(str, unique=True)
  password = Required(str)
  dek = Optional(bytes)
  dek_nonce = Optional(bytes)
  data = Optional(bytes)
  data_nonce = Optional(bytes)


def encrypt_password(password):
  return bcrypt(password, 12).decode('ascii')


def check_password(*, raw, encrypted):
  try:
    bcrypt_check(raw, encrypted)
    return True
  except:
    return False

_KEK = None
def get_kek() -> bytes:
  global _KEK
  if _KEK is None:
    with open('kek.txt', 'rb') as f:
      _KEK = f.read()
  return _KEK


def decrypt(*, key: bytes, encrypted: bytes, nonce: bytes) -> bytes:
  return AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt(encrypted)


def encrypt(*, key: bytes, data: bytes):
  aes = AES.new(key, AES.MODE_GCM)
  return aes.encrypt(data), aes.nonce


def get_auth_page(name, write=False):
  write_field = '<input type="text" name="data" placeholder="Sensitive data" />'

  return f'''
<form method="post" action="">
  <input type="text" name="login" placeholder="Login" required />
  <input type="password" name="password" placeholder="Password" required />
  {write_field if write else ''}
  <input type="submit" value="{name}" />
</form>
'''

def validate_password(password):
  if not (8 <= len(password) <= 64):
    return 'Invalid length (must be in a range [8; 64])'

  if not any(el in password for el in string.punctuation):
    return 'Does not have any punctuation characters: ' + string.punctuation

  if not any(el in password for el in string.ascii_lowercase):
    return 'Does not have any lowercase characters'

  if not any(el in password for el in string.ascii_uppercase):
    return 'Does not have any uppercase characters'

  if not any(el in password for el in string.digits):
    return 'Does not have any numbers'


@app.route('/')
def home():
  return '''<a href="/read">Read sensitive data</a>
  <br />
  <a href="/write">Write sensitive data</a>
  <br />
  <a href="/register">Register</a>
  '''


@app.route('/read', methods=['GET'])
def read_page():
  return get_auth_page('Login')


@app.route('/read', methods=['POST'])
def read_data():
  login, password = request.form['login'], request.form['password']

  validation = validate_password(password)
  if validation:
    return make_response(validation, 403)

  user: User = User.get(login=login)
  if not user or not check_password(raw=password, encrypted=user.password):
    return make_response('Login and/or password is invalid', 403)

  if user.data is None:
    return 'No data is available'

  dek = decrypt(key=get_kek(), encrypted=user.dek, nonce=user.dek_nonce)
  return decrypt(key=dek, encrypted=user.data, nonce=user.data_nonce).decode('utf-8')


@app.route('/write', methods=['GET'])
def write_page():
  return get_auth_page('Login', write=True)


@app.route('/write', methods=['POST'])
def write_data():
  login, password = request.form['login'], request.form['password']
  data: bytes = request.form['data'].encode('utf-8')

  validation = validate_password(password)
  if validation:
    return make_response(validation, 403)

  user: User = User.get(login=login)
  if not user or not check_password(raw=password, encrypted=user.password):
    return make_response('Login and/or password is invalid', 403)

  if len(data) > 255:
    return 'Data is too long (must be at most 255 ascii letters)'

  dek = get_random_bytes(32)
  user.dek, user.dek_nonce = encrypt(key=get_kek(), data=dek)
  user.data, user.data_nonce = encrypt(key=dek, data=data)
  return 'Success'


@app.route('/register', methods=['GET'])
def register_page():
  return get_auth_page('Register')


@app.route('/register', methods=['POST'])
def register_user():
  login, password = request.form['login'], request.form['password']

  validation = validate_password(password)
  if validation:
    return make_response(validation, 403)

  if User.get(login=login):
    return make_response('Login already exists', 403)

  User(login=login, password=encrypt_password(password))
  return 'Success'


db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

if __name__ == '__main__':
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  context.load_dh_params('dhparams.pem')
  ciphersuite = (
    'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256'
    ':DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256'
    ':!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!DSS:!RC4:!SEED:!ECDSA:!ADH:!IDEA:!3DES'
  )
  context.set_ciphers(ciphersuite)
  context.load_cert_chain('cert.pem', 'key.pem')
  app.run(ssl_context=context)
