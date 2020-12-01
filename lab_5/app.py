from flask import Flask, request, make_response
import string
from pony.flask import Pony
from pony.orm import Required, Database
from Crypto.Protocol.KDF import bcrypt, bcrypt_check


app = Flask(__name__)
app.config['PONY'] = {
  'provider': 'mysql',
  'host': 'localhost',
  'user': 'vasniktel',
  'passwd': 'vasniktel',
  'db': 'crypto_lab_5'
}

db = Database()
Pony(app)


class User(db.Entity):
  login = Required(str, unique=True)
  password = Required(str)

  def __repr__(self) -> str:
    return f'<User login={self.login} password={self.password}>'

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)


def encrypt_password(password):
  return bcrypt(password, 12).decode('ascii')


def check_password(*, raw, encrypted):
  try:
    bcrypt_check(raw, encrypted)
    return True
  except:
    return False


def get_auth_page(name):
  return f'''
<form method="post" action="">
  <input type="text" name="login" placeholder="Login" required />
  <input type="password" name="password" placeholder="Password" required />
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
  return '<a href="/login">Login</a><br /><a href="/register">Register</a>'


@app.route('/login', methods=['GET'])
def login_page():
  return get_auth_page('Login')


@app.route('/login', methods=['POST'])
def login_user():
  login, password = request.form['login'], request.form['password']

  validation = validate_password(password)
  if validation:
    return make_response(validation, 403)

  user = User.get(login=login)
  if not user or not check_password(raw=password, encrypted=user.password):
    return make_response('Login and/or password is invalid', 403)

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
